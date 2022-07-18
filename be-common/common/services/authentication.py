from datetime import datetime
import os

from ecdsa import VerifyingKey
from jose import jwt, JWTError

from common.types.exception import UnauthorizedException


ACCESS_TOKEN_ALGORITHM = "ES256"
ACCESS_TOKEN_PUBLIC_KEY_PEM = os.environ.get(
    "TOKEN_PUBLIC_KEY_PEM",
"""
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEnoH4lyjW4T0uUFbAYRL1G/3dxF1M
kak4CYTwDU8lSubpkIKXFqo7KtsWIycbTKbfLm2IdwNXDOO346u4OhCaBg==
-----END PUBLIC KEY-----
""",
)
ACCESS_TOKEN_PUBLIC_KEY = VerifyingKey.from_pem(TOKEN_PUBLIC_KEY_PEM)


class AuthenticationService:
    def verify_and_parse_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, ACCESS_TOKEN_PUBLIC_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        except JWTError:
            raise UnauthorizedException()
        
        if (payload["exp"] - int(datetime.utcnow().timestamp()) < 0):
            raise UnauthorizedException()

        return payload
