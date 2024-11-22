from fastapi import UploadFile, HTTPException
from app.validators.base_validator import BaseValidator

class SizeValidator(BaseValidator):
    """
    This subclass of BaseValidator checks whether the file size is valid or not given a max file size in MB.

    Attributes
    ----------
    max_size : int
        The maximum allowed file size in MB

    Methods
    -------
    validate_file(file: UploadFile) -> bool
        Validates the file size
    """

    def __init__(self, max_size):
        self.max_bytes = 1024 * 1024 * max_size

    def validate(self, file: UploadFile):
        """
        Validates the size of the file.

        Arguments:
            file (UploadFile): The file to validate

        Returns:
            True if the file size is valid

        Raises:
            HTTPException: If the file size is too large or is empty
        """
        file.file.seek(0, 2) # Go to the end of the file
        file_size = file.file.tell() # Store the file size
        file.file.seek(0) # Go back to the start of the file

        if file_size > self.max_bytes:
            raise HTTPException(
                status_code=413,
                detail=
                f"File size is too large ({round(file_size/1048576,2)} MB). File size must not exceed {self.max_bytes/1048576} MB."
            )
        elif file_size == 0:
            raise HTTPException(
                status_code=413,
                detail=
                f"File must not be empty."
            )

        return True