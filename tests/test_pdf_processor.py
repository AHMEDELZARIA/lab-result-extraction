import pytest
from fastapi import UploadFile, HTTPException
from app.processors.pdf_processor import PDFProcessor

@pytest.fixture
def processor():
    file_path = "tests/lab-result.pdf"

    with open(file_path, "rb") as f:
        uploaded_file = UploadFile(filename="test.pdf", file=f)

        processor = PDFProcessor(uploaded_file)

    return processor

def test_valid_pdf(processor):
    assert processor._validate() is not HTTPException

def test_valid_parsing(processor):
    assert processor.extract_text() is not HTTPException


