from fastapi import UploadFile, HTTPException
from app.validators.base_validator import BaseValidator

class MimeValidator(BaseValidator):
    """
    This subclass of BaseValidator checks whether the mime type of the file is valid or not given a list of allowed
    mimes.

    Attributes:
        allowed_mimes (list): List of allowed mime types.

    Methods:
        validate(extension_file: UploadFile): Validates the mime type of file.
    """

    def __init__(self, allowed_mimes):
        self.allowed_mimes = allowed_mimes

    def validate(self, file: UploadFile):
        """
        Validates the mime type of the file.

        :param file: The file to validate.
        :return: True if the mime type is valid, else raise an HTTPException.
        """
        if file.content_type not in self.allowed_mimes:
            raise HTTPException(
                status_code=400,
                detail=f"Extension must be one of {self.allowed_mimes}"
            )

        return True