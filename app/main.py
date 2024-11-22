# Core FastAPI framework
from fastapi import FastAPI, UploadFile, File, HTTPException

from aiolimiter import AsyncLimiter

from app.validators.composite_validator import CompositeValidator
from app.validators.extention_validator import ExtensionValidator
from app.validators.mime_validator import MimeValidator
from app.validators.size_validator import SizeValidator
from app.processors.pdf_processor import PDFProcessor
from app.models.openai_models import OpenAIModel

# Initialize the FastAPI application
app = FastAPI()

# Set a limit of 10 requests per minute
limiter = AsyncLimiter(max_rate=10, time_period=60)

@app.get("/")
async def root():
    """
    Root endpoint, redirect to /extract
    """
    return {"message": "Welcome to the Lab Results extraction API for the Medsender Challenge. Visit /docs for an interface to use the extract endpoint."}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    """
    Given a valid lab result file, the following fields are extracted (if a field is not present, it will have a default value of "not present"):
    - Patient Name
    - Patient Date of Birth (DOB)
    - Patient Address
    - Patient Gender
    - Ordering Physician Name
    """
    async  with limiter:
        # Configure the file handling validator to accept only pdfs, no larger than 10 MBs
        validator = CompositeValidator([
            ExtensionValidator(['pdf']),
            MimeValidator(['application/pdf']),
            SizeValidator(10)
        ])

        try:
            # Perform file handling validations
            validator.validate(file)

            # Process the pdf and extract the text in Markdown format
            # Markdown is a format easily understood by LLMs
            pdf_processor = PDFProcessor(file)
            text = await pdf_processor.extract_text()

            # Prompt an OpenAI model to extract the required fields in json format
            model = OpenAIModel("gpt-4o-mini")
            result = model.get_fields(text)

            return result
        except Exception as e:
            return HTTPException(
                status_code=500, detail=str(e)
            )
