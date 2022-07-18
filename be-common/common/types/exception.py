class AradException(Exception):
    def __init__(self, message="Internal server error"):
        super().__init__(message)

class UnauthorizedException(AradException):
    pass
