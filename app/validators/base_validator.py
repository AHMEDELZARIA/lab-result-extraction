from fastapi import UploadFile

class BaseValidator:
    """
    Base validator class that all validators must inherit from.
    """

    def __init__(self):
        pass

    def validate(self, file: UploadFile):
        raise NotImplementedError("Subclasses must implement this method")