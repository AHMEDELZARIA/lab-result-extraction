from app.processors.base_processor import BaseProcessor
from fastapi import HTTPException, UploadFile
from llama_parse import LlamaParse
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import pdfplumber
import tempfile
import shutil
import fitz
import os

class PDFProcessor(BaseProcessor):
    """
    PDFProcessor is a subclass of BaseProcessor which takes a PDF file as input, validates the pdf content, then can
    extract the text from the pdf, regardless if it OCR or native.

    Attributes
    ----------
    file : UploadFile
        pdf file to validate and extract text from

    Methods
    -------
    _create_tmp_file() -> str
        Creates a temporary file
    _validate() -> None
        Validates the pdf file
    _check_file_malformed() -> None
        Checks if the pdf file is malformed
    _check_file_empty() -> None
        Checks if the pdf file is empty
    _check_file_encryption() -> None
        checks if the pdf file is encrypted
    extract_text() -> str
        extracts the text from the pdf file in markdown format
    _cleanup() -> None
        cleans up the temporary file for security purposes
    """

    def __init__(self, file: UploadFile):
        self.file = file
        self.tmp_filepath = self._create_tmp_file()

    def _create_tmp_file(self):
        """
        Creates a temporary file to store the pdf

        Returns:
            tmp_filepath (str): temporary file path to store the pdf

        Raises:
            HTTPException: if the temporary file cannot be created
        """
        try:
            tmp_dir = tempfile.gettempdir()
            tmp_filepath = os.path.join(tmp_dir, self.file.filename)
            with open(tmp_filepath, "wb") as temp_file:
                shutil.copyfileobj(self.file.file, temp_file)

            return tmp_filepath
        except:
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error, could not create tmp file.",
            )

    def _validate(self):
        """
        Validates the pdf file before extracting text from it

        Raises:
            HTTPException: if the pdf is not valid
        """
        self._check_file_malformed()
        self._check_file_encryption()
        self._check_file_empty()

    def _check_file_malformed(self):
        """
        Checks if the pdf file is malformed.

        Raises:
            HTTPException: if the pdf file is malformed
        """
        try:
            reader = PdfReader(self.tmp_filepath)
            _ = reader.pages # Unused var but triggers parsing
        except:
            raise HTTPException(
                status_code=400,
                detail="File is malformed."
            )

    def _check_file_encryption(self):
        """
        Checks if the pdf file is encrypted

        Raises:
            HTTPException: if the pdf file is encrypted
        """
        try:
            pdf = fitz.Document(self.tmp_filepath)
            if pdf.needs_pass:
                raise Exception("File is encrypted. Cannot process encrypted files.")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"{str(e)}"
            )

    def _check_file_empty(self):
        """
        Checks if the pdf file is empty

        Raises:
            HTTPException: if the pdf file is empty
        """
        try:
            with pdfplumber.open(self.tmp_filepath) as pdf:
                # Check if pdf is completely empty
                if not pdf.pages:
                    raise Exception("PDF file is empty.")

                # Check if pdf has no text
                text_available = False
                for page in pdf.pages:
                    if page.extract_text():
                        text_available = True
                        break
                if not text_available:
                    raise Exception("PDF file does not contain any readable text.")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"{str(e)}"
            )

    async def extract_text(self):
        """
        Extracts the text from the pdf file in Markdown format for LLMs to easily process.

        Returns:
            extracted_text (str): extracted text from the pdf file in Markdown format

        Raises:
            HttpException: if could not extract text from pdf file
        """
        try:
            # Validate the content of the pdf
            self._validate()

            # Load the llama parse api key
            load_dotenv()
            llama_parse_key = os.getenv("LLAMA_PARSE_API_KEY")

            # Load the llama parse instructions for more accurate text extraction
            with open("app/prompts/llama_parser_prompt.txt", "r") as llama_prompt:
                parsing_instructions = llama_prompt.read()

            # Initialize the parser
            parser = LlamaParse(
                api_key=f"{llama_parse_key}",
                parsing_instruction=parsing_instructions,
                result_type="markdown"
            )

            # Parse the pdf
            parsed_text = await parser.aload_data(self.tmp_filepath)
            extracted_text = parsed_text[0].text

            return extracted_text
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"{str(e)}"
            )
        finally:
            # Discard the pdf for security reasons
            self._cleanup()

    def _cleanup(self):
        """
        Removes the temporary file after use for security purpose (not storing sensitive data)
        """
        if os.path.exists(self.tmp_filepath):
            os.remove(self.tmp_filepath)
