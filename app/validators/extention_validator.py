from fastapi import UploadFile, HTTPException
from app.validators.base_validator import BaseValidator

class ExtensionValidator(BaseValidator):
    """
    This subclass of BaseValidator checks whether the file extension is valid or not given a list of allowed extensions.

    Attributes:
        allowed_extensions (list): List of allowed file extensions.

    Methods:
        validate(extension_file: UploadFile): Validates the extension file.
    """

    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def validate(self, file: UploadFile):
        """
        Validates the extension file.

        :param file: The file to validate.
        :return: True if the extension is valid, else raise an HTTPException.
        """
        for extension in self.allowed_extensions:
            if file.filename.lower().endswith(extension):
                return True

        raise HTTPException(
            status_code=400,
            detail=f"Extension '{file.filename}' is not allowed"
        )