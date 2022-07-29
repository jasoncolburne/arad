import fastapi
import fastapi.security
import sqlmodel

import common.app
import common.datatypes.domain
import common.datatypes.exception
import common.datatypes.response
import common.services.authorization
import database

import identity.datatypes.request
import identity.datatypes.response
import identity.orchestrations


app = common.app.get_application()
oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/identify/token")


@app.get(
    "/health",
    include_in_schema=False,
    response_model=common.datatypes.response.HealthCheckResponse,
)
async def health() -> common.datatypes.response.HealthCheckResponse:
    return common.datatypes.response.HealthCheckResponse(status="ok")


@app.post("/register", response_model=identity.datatypes.response.RegisterResponse)
async def register(
    request: identity.datatypes.request.RegisterRequest,
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.RegisterResponse:
    try:
        return await identity.orchestrations.arad_register(
            email=request.email,
            passphrase=request.passphrase,
            database=_database,
        )
    except common.datatypes.exception.BadRequestException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        ) from exc


@app.post("/login", response_model=identity.datatypes.response.LoginResponse)
async def login(
    request: identity.datatypes.request.LoginRequest,
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.LoginResponse:
    try:
        return await identity.orchestrations.arad_login(
            email=request.email,
            passphrase=request.passphrase,
            database=_database,
        )
    except common.datatypes.exception.UnauthorizedException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        ) from exc


@app.post("/logout", response_model=identity.datatypes.response.LogoutResponse)
async def logout(
    request: identity.datatypes.request.LogoutRequest,
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.LogoutResponse:
    return await identity.orchestrations.arad_logout(
        refresh_token=request.refresh_token, database=_database
    )


@app.post("/token", response_model=identity.datatypes.response.TokenResponse)
async def access_token(
    request: identity.datatypes.request.TokenRequest,
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.TokenResponse:
    try:
        return await identity.orchestrations.arad_access_token(
            refresh_token=request.refresh_token,
            scope=request.scope,
            database=_database,
        )
    except common.datatypes.exception.UnauthorizedException as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        ) from exc


@app.get("/roles", response_model=identity.datatypes.response.RolesResponse)
@common.services.authorization.require_authorization(
    common.datatypes.domain.Role.ADMINISTRATOR
)
async def roles(
    token: str = fastapi.Depends(oauth2_scheme),  # pylint: disable=unused-argument
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.RolesResponse:
    return await identity.orchestrations.arad_roles(database=_database)


@app.put("/role", response_model=identity.datatypes.response.RoleResponse)
@common.services.authorization.require_authorization(
    common.datatypes.domain.Role.ADMINISTRATOR
)
async def assign_role(
    request: identity.datatypes.request.RoleRequest,
    token: str = fastapi.Depends(oauth2_scheme),  # pylint: disable=unused-argument
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.RoleResponse:
    return await identity.orchestrations.arad_modify_role_assignment(
        user_id=request.user_id,
        role=request.role,
        action=request.action,
        database=_database,
    )


@app.post("/users", response_model=identity.datatypes.response.UsersResponse)
@common.services.authorization.require_authorization(
    common.datatypes.domain.Role.ADMINISTRATOR
)
async def users(
    request: identity.datatypes.request.UsersRequest,
    token: str = fastapi.Depends(oauth2_scheme),  # pylint: disable=unused-argument
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> identity.datatypes.response.UsersResponse:
    return await identity.orchestrations.arad_users(
        email_filter=request.email_filter,
        page=request.page,
        database=_database,
        user_service=None,
    )
