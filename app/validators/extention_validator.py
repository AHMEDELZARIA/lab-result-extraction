from app.validators.base_validator import BaseValidator
from fastapi import UploadFile, HTTPException

class ExtensionValidator(BaseValidator):
    """
    This subclass of BaseValidator checks whether the file extension is valid or not given a list of allowed extensions.

    Attributes
    ----------
    allowed_extensions : list of str
        List of allowed file extensions

    Methods
    -------
    validate(extension_file: UploadFile) -> bool
        Validates the extension of the uploaded file against a list of allowed extensions
    """

    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def validate(self, file: UploadFile):
        """
        Validates the extension of the uploaded file against a list of allowed extensions

        Arguments:
            file (UploadFile): The file to validate

        Returns:
            True if the extension is valid

        Raises:
            HTTPException: if the file does not contain any of the allowed extensions
        """
        for extension in self.allowed_extensions:
            if file.filename.lower().endswith(extension):
                return True

        raise HTTPException(
            status_code=400,
            detail=f"Extension '{file.filename}' is not allowed"
        )