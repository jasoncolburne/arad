# Make sure you are editing this file in arad/core


class AradException(Exception):
    pass


class BadRequestException(AradException):
    pass


class UnauthorizedException(AradException):
    pass
