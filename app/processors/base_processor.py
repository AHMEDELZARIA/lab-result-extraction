class BaseProcessor:
    """
    Base processor class that all processors must inherit from.
    """

    def __init__(self):
        pass

    def _validate(self):
        """
        Should validate the content of the file before extracting text.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def extract_text(self):
        """
        Should extract the content of the file after validating it via _validate().
        """
        raise NotImplementedError("Subclasses must implement this method")