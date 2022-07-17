from fastapi import Depends, HTTPException, status
from sqlalchemy import exc
from sqlmodel import Session

from common.app import get_application
from common.services.role import RoleService
from common.services.user import UserService
from common.types.exception import UnauthorizedException
from common.types.response import User as UserType
from database import get_session
from database.models import User

from .services.authentication import AuthenticationService
from .types.request import LoginRequest, RegisterRequest, TokenRequest
from .types.response import LoginResponse, RegisterResponse, TokenResponse


app = get_application()


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy?"}



@app.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, database: Session = Depends(get_session)):
    authentication_service = AuthenticationService(database=database)
    try:
        user = await authentication_service.create_user_with_passphrase(
            email=request.email,
            passphrase=request.passphrase,
        )
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        )

    refresh_token = await authentication_service.create_refresh_token(user=user)

    role_service = RoleService(database=database)
    roles = await role_service.all_for_user(user=user)
    
    return {
        "refresh_token": refresh_token,
        "user": user,
        "roles": roles
    }


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, database: Session = Depends(get_session)):
    authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    authentication_service = AuthenticationService(database=database)
    try:
        user = await authentication_service.authenticate_by_passphrase(
            email=request.email,
            passphrase=request.passphrase,
        )
    except (exc.NoResultFound, UnauthorizedException):
        raise authentication_exception

    refresh_token = await authentication_service.create_refresh_token(user=user)

    role_service = RoleService(database=database)
    roles = await role_service.all_for_user(user=user)
    
    return {
        "refresh_token": refresh_token,
        "user": user,
        "roles": roles
    }


@app.post("/token", response_model=TokenResponse)
async def token(request: TokenRequest, database: Session = Depends(get_session)):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
    )
    
    authentication_service = AuthenticationService(database=database)
    try:
        user_id = await authentication_service.verify_and_extract_uuid_from_refresh_token(
            refresh_token=request.refresh_token
        )
    except UnauthorizedException:
        raise unauthorized_exception

    role_service = RoleService(database=database)
    # this is pretty nasty, constructing a user without an email because we know we won't be using it
    roles = await role_service.all_for_user(user=UserType(id=user_id, email=''))
    if request.scope not in roles:
        raise unauthorized_exception

    access_token = authentication_service.create_access_token(user_id=user_id, scope=request.scope)
    return {"access_token": access_token}

