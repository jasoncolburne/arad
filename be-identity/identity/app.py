from fastapi import Depends, HTTPException, status
from sqlalchemy import exc
from sqlmodel import Session

from common.app import get_application
from common.services.role import RoleService
from common.services.user import UserService
from common.types.exception import AradException
from database import get_session
from database.models import User

from .services.authentication import AuthenticationService
from .types.response import LoginResponse, RegisterResponse


app = get_application()


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy?"}



@app.post("/register", response_model=RegisterResponse)
async def register(body: dict, database: Session = Depends(get_session)):
    email = body['email']
    passphrase = body['passphrase']

    authentication_service = AuthenticationService(database=database)
    try:
        user = await authentication_service.create_user_with_passphrase(email=email, passphrase=passphrase)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        )

    role_service = RoleService()
    roles = role_service.list_current(user)
    access_token = authentication_service.create_access_token(user)
    return {
        "credentials": {"token": access_token, "token_type": "bearer"},
        "user": {"id": user.id, "email": user.email},
        "roles": roles,
    }


@app.post("/login", response_model=LoginResponse)
async def login(body: dict, database: Session = Depends(get_session)):
    authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = body['email']
    passphrase = body['passphrase']

    authentication_service = AuthenticationService(database=database)
    try:
        user = await authentication_service.authenticate_by_passphrase(email=email, passphrase=passphrase)
    except (exc.NoResultFound, AradException):
        raise authentication_exception

    role_service = RoleService()
    roles = role_service.list_current(user)
    access_token = authentication_service.create_access_token(user)
    return {
        "credentials": {"token": access_token, "token_type": "bearer"},
        "user": {"id": user.id, "email": user.email},
        "roles": roles,
    }
