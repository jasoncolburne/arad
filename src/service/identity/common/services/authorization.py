# Make sure you are editing this file in arad/core

import datetime
import os

import ecdsa
import jose
from jose import jwt

import common.datatypes.domain
import common.datatypes.exception


ACCESS_TOKEN_ALGORITHM = "ES384"
ACCESS_TOKEN_PUBLIC_KEY_PEM = os.environ.get("ACCESS_TOKEN_PUBLIC_KEY_PEM")
ACCESS_TOKEN_PUBLIC_KEY = ecdsa.VerifyingKey.from_pem(ACCESS_TOKEN_PUBLIC_KEY_PEM)


class AuthorizationService:
    def verify_and_parse_token(self, token: str) -> common.datatypes.domain.Token:
        try:
            payload = jwt.decode(
                token, ACCESS_TOKEN_PUBLIC_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
            )
        except jose.JWTError as exc:
            raise common.datatypes.exception.UnauthorizedException() from exc

        try:
            if payload["exp"] - int(datetime.datetime.utcnow().timestamp()) < 0:
                raise common.datatypes.exception.UnauthorizedException()
        except KeyError as exc:
            raise common.datatypes.exception.UnauthorizedException() from exc

        return common.datatypes.domain.Token(**payload)
