from fastapi import UploadFile

class BaseValidator:
    """
    Base validator class that all validators must inherit from. Each validator must inherit from this class and implement
    the `validate()` method.

    Methods:
        validate(file: UploadFile): Validates the uploaded file
    """

    def validate(self, file: UploadFile):
        raise NotImplementedError("Subclasses must implement this method")