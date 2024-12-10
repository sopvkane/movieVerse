class ValidationError(Exception):
    """Custom exception class for model validation errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message
