class Error(Exception):
    """Base class"""
    pass


class TokenGenerateError(Error):

    def __init__(self, message):
        self.message = message
