from pydantic import BaseModel


class AuthenticationRequest(BaseModel):
    email: str
    passphrase: str


class RegisterRequest(AuthenticationRequest):
    pass


class LoginRequest(AuthenticationRequest):
    pass
