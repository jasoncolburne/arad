class AradException(Exception):
    def __init__(self, message="Internal server error"):
        super().__init__(message)

class BadRequestException(AradException):
    pass

class UnauthorizedException(AradException):
    pass
