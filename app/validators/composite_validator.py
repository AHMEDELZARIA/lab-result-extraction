from fastapi import UploadFile
from app.validators.base_validator import BaseValidator


class CompositeValidator(BaseValidator):
    """
    This subclass of BaseValidator takes in a list of validators and validates the file on specified validators.

    Attributes:
        validators (list): A list of validators.

    Methods:
        validate(path): Validates the file on specified validators.
    """

    def __init__(self, validators):
        self.validators = validators

    def validate(self, file: UploadFile):
        """
        Validates the file on specified validators.

        :param file: the file to validate.
        :return: True if the file is valid, HTTPException otherwise.
        """
        for validator in self.validators:
            validator.validate(file)