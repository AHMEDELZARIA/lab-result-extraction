import pytest
from fastapi import UploadFile, HTTPException
from io import BytesIO
from app.validators.extention_validator import ExtensionValidator

@pytest.fixture
def extension_validator():
    return ExtensionValidator(['pdf'])

def test_is_pdf(extension_validator):
    # Make a mock, valid, pdf file
    mock_pdf = UploadFile(filename="test.pdf", file=BytesIO(b"Mock pdf file"))

    # Assert that the mock pdf is recognized as a valid pdf
    assert extension_validator.validate(mock_pdf) is True

def test_is_not_pdf(extension_validator):
    # Make a mock, non-pdf file
    mock_non_pdf = UploadFile(filename="test.txt", file=BytesIO(b"Mock test file"))

    # Assert that the correct exception is raised
    with pytest.raises(HTTPException) as e:
        extension_validator.validate(mock_non_pdf)
    assert e.value.status_code == 400