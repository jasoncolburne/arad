import logging
from functools import wraps

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlmodel import Session

from common.app import get_application
from common.services.authentication import AuthenticationService
from common.services.user import UserService
from common.types.response import Role
from common.types.exception import UnauthorizedException
from database import get_session

from .types.request import UsersRequest
from .types.response import UsersResponse


app = get_application()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/identify/login")
authentication_service = AuthenticationService()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def require_authorization(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            token = kwargs["token"]
            token_contents = authentication_service.verify_and_parse_token(token=token)
        except UnauthorizedException:
            raise credentials_exception

        if token_contents.get("scope") != str(Role.ADMINISTRATOR):
            raise credentials_exception

        return await func(*args, **kwargs)

    return wrapper


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy?"}


@app.post("/users", response_model=UsersResponse)
@require_authorization
async def users(
    request: UsersRequest,
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    user_service = UserService(database=database)
    return await user_service.page(number=request.page)
