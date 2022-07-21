import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import exc
from sqlmodel import Session

from common.app import get_application
from common.services.authorization import require_authorization
from common.services.user import UserService
from common.types.exception import UnauthorizedException
from common.types.response import User, Role
from database import get_session

from .services.authentication import AuthenticationService
from .services.role import RoleService
from .types.request import LoginRequest, RegisterRequest, TokenRequest, RoleRequest, RoleAction
from .types.response import LoginResponse, RegisterResponse, TokenResponse, RolesResponse, RoleResponse


DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL")

app = get_application()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/identify/token")


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

    role_service = RoleService(database=database)
    await role_service.assign_for_user(user=user, role=Role.READER)

    if DEFAULT_ADMIN_EMAIL and request.email == DEFAULT_ADMIN_EMAIL:
        await role_service.assign_for_user(user=user, role=Role.REVIEWER)
        await role_service.assign_for_user(user=user, role=Role.ADMINISTRATOR)

    return await _authentication_response(database=database, user=user, authentication_service=authentication_service)


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

    return await _authentication_response(database=database, user=user, authentication_service=authentication_service)


async def _authentication_response(database: Session, user: User, authentication_service: AuthenticationService):
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

    try:
        access_token = await authentication_service.create_access_token(user_id=user_id, scope=request.scope)
    except UnauthorizedException:
        raise unauthorized_exception

    return {"access_token": access_token}


@app.get("/roles", response_model=RolesResponse)
@require_authorization(Role.ADMINISTRATOR)
async def roles(
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    role_service = RoleService(database=database)
    roles = await role_service.all()
    return {"roles": roles}


@app.put("/role", response_model=RoleResponse)
@require_authorization(Role.ADMINISTRATOR)
async def assign_role(
    request: RoleRequest,
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    role_service = RoleService(database=database)
    user_service = UserService(database=database)

    user = await user_service.get(user_id=request.user_id)

    # this admin function isn't critical and the ui should protect us from most edge cases so we'll just let these
    # calls explode if for instance the role has already been assigned to the user (possible with two tabs open)
    if request.action == RoleAction.ASSIGN:
        role = await role_service.assign_for_user(user=user, role=request.role)
    elif request.action == RoleAction.REVOKE:
        role = await role_service.revoke_for_user(user=user, role=request.role)
    else:
        # this code should be unreachable
        raise Exception()

    # TODO: log user out by removing/denylisting refresh tokens

    return {"role": role}
