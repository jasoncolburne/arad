import os

from ecdsa import VerifyingKey
from jose import jwt, JWTError


TOKEN_EXPIRATION_MINUTES = 15
TOKEN_ALGORITHM = "ES256"
TOKEN_PUBLIC_KEY_PEM = os.environ.get(
    "TOKEN_PUBLIC_KEY_PEM",
"""
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEnoH4lyjW4T0uUFbAYRL1G/3dxF1M
kak4CYTwDU8lSubpkIKXFqo7KtsWIycbTKbfLm2IdwNXDOO346u4OhCaBg==
-----END PUBLIC KEY-----
""",
)
TOKEN_PUBLIC_KEY = VerifyingKey.from_pem(TOKEN_PUBLIC_KEY_PEM)


class AuthenticationService:
    def verify_and_parse_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, TOKEN_PUBLIC_KEY, algorithms=[TOKEN_ALGORITHM])
        except JWTError:
            raise UnauthorizedException("Could not validate credentials")
        
        return payload