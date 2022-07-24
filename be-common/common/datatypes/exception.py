class AradException(Exception):
    pass
    # def __init__(self, message: str = "Internal server error"):
    #     super().__init__(message)


class BadRequestException(AradException):
    pass


class UnauthorizedException(AradException):
    pass
