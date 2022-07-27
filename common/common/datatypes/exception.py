class AradException(Exception):
    pass


class BadRequestException(AradException):
    pass


class UnauthorizedException(AradException):
    pass
