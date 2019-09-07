class Error(Exception):
    """Base class"""
    pass


class TokenGenerateError(Error):
    """
    토큰 생성 에러

    :param: message: 에러 메세지
    """
    def __init__(self, message):
        self.message = message


class ConnectedIdGenerateError(Error):
    """
    커넥티드 아이디 생성 에러

    :param: message: 에러 메세지
    """
    def __init__(self, message):
        self.message = message
