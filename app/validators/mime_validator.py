from fastapi import UploadFile, HTTPException
from app.validators.base_validator import BaseValidator

class MimeValidator(BaseValidator):
    """
    This subclass of BaseValidator checks whether the mime type of the file is valid or not given a list of allowed
    mimes.

    Attributes
    ----------
    allowed_mimes : list of str
        List of allowed mime types.

    Methods
    -------
    validate(extension_file: UploadFile) -> bool
        Validates the file mime type
    """

    def __init__(self, allowed_mimes):
        self.allowed_mimes = allowed_mimes

    def validate(self, file: UploadFile):
        """
        Validates the mime type of the file

        Arguments:
            file (UploadFile): the file to be validated

        Returns:
            True if the mime type of the file is valid

        Raises:
            HTTPException: if the mime type of the file is invalid
        """
        if file.content_type not in self.allowed_mimes:
            raise HTTPException(
                status_code=400,
                detail=f"Extension must be one of {self.allowed_mimes}"
            )

        return True