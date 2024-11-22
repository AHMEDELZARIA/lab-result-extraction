import pytest
from fastapi import UploadFile, HTTPException
from io import BytesIO
from app.validators.size_validator import SizeValidator

def test_valid_size():
    # Mock a file smaller than max size
    content = b"0" * (1024 * 1024) # 1024 KB
    mock_pdf = UploadFile(filename="test.pdf", file=BytesIO(content))

    size_validator = SizeValidator(10)
    assert size_validator.validate(mock_pdf) is True

def test_invalid_size():
    # Mock a file larger than max size
    content = b"0" * (1024 * 1024)  # 1024 KB
    mock_non_pdf = UploadFile(filename="test.pdf", file=BytesIO(content))

    size_validator = SizeValidator(0.5)
    # Assert that the correct exception is raised
    with pytest.raises(HTTPException) as e:
        size_validator.validate(mock_non_pdf)
    assert e.value.status_code == 413
    assert f"Extension '{mock_non_pdf.filename}' is not allowed"