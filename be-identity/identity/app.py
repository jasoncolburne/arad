from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from common.app import get_application
from common.services.authorization import require_authorization
from common.datatypes.exception import BadRequestException, UnauthorizedException
from common.datatypes.response import Role, HealthCheckResponse
from database import get_session

from .datatypes.request import (
    LoginRequest,
    RegisterRequest,
    TokenRequest,
    RoleRequest,
    LogoutRequest,
)
from .datatypes.response import (
    LoginResponse,
    RegisterResponse,
    TokenResponse,
    RolesResponse,
    RoleResponse,
    LogoutResponse,
)
from .orchestrations import (
    arad_register,
    arad_login,
    arad_logout,
    arad_access_token,
    arad_roles,
    arad_assign_role,
)


app = get_application()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/identify/token")


@app.get("/health", include_in_schema=False, response_model=HealthCheckResponse)
async def health() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")


@app.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest, database: Session = Depends(get_session)
) -> RegisterResponse:
    try:
        return await arad_register(
            email=request.email,
            passphrase=request.passphrase,
            database=database,
        )
    except BadRequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        ) from exc


@app.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest, database: Session = Depends(get_session)
) -> LoginResponse:
    try:
        return await arad_login(
            email=request.email,
            passphrase=request.passphrase,
            database=database,
        )
    except UnauthorizedException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        ) from exc


@app.post("/logout", response_model=LogoutResponse)
async def logout(
    request: LogoutRequest,
    database: Session = Depends(get_session),
) -> LogoutResponse:
    return await arad_logout(refresh_token=request.refresh_token, database=database)


@app.post("/token", response_model=TokenResponse)
async def access_token(
    request: TokenRequest, database: Session = Depends(get_session)
) -> TokenResponse:
    try:
        return await arad_access_token(
            refresh_token=request.refresh_token,
            scope=request.scope,
            database=database,
        )
    except UnauthorizedException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        ) from exc


@app.get("/roles", response_model=RolesResponse)
@require_authorization(Role.ADMINISTRATOR)
async def roles(
    token: str = Depends(oauth2_scheme),  # pylint: disable=unused-argument
    database: Session = Depends(get_session),
) -> RolesResponse:
    return await arad_roles(database=database)


@app.put("/role", response_model=RoleResponse)
@require_authorization(Role.ADMINISTRATOR)
async def assign_role(
    request: RoleRequest,
    token: str = Depends(oauth2_scheme),  # pylint: disable=unused-argument
    database: Session = Depends(get_session),
) -> RoleResponse:
    return await arad_assign_role(
        user_id=request.user_id,
        role=request.role,
        action=request.action,
        database=database,
    )
