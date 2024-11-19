from fastapi import UploadFile, HTTPException
from app.validators.base_validator import BaseValidator

class SizeValidator(BaseValidator):
    """
    This subclass of BaseValidator checks whether the file size is valid or not given a max file size in MB.

    Attributes:
        max_size (int): The maximum allowed file size.

    Methods:
        validate_file(file: UploadFile): Validates the file size
    """

    def __init__(self, max_size):
        self.max_bytes = 1024 * 1024 * max_size

    def validate(self, file: UploadFile):
        """
        Validates the size of the file.

        :param file: The file to validate.
        :return: True if the file size is valid, else raise an HTTPException.
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

        return True