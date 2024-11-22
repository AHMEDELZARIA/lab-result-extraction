from fastapi import UploadFile
from app.validators.base_validator import BaseValidator


class CompositeValidator(BaseValidator):
    """
    This subclass of BaseValidator takes in a list of validators and validates the file on specified validators.

    Attributes
    ----------
    validators : list of validator objects
        A list of validators

    Methods
    -------
    validate(file: UploadFile) -> None
        Validates the file on specified validators
    """

    def __init__(self, validators):
        self.validators = validators

    def validate(self, file: UploadFile):
        """
        Validates the file on specified validators.

        Arguments:
            file (UploadFile): The file to validate

        Raises:
            Exception: If any of the validators are invalid
        """
        for validator in self.validators:
            validator.validate(file)