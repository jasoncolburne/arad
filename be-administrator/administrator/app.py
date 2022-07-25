import fastapi
import fastapi.security
import sqlmodel

import common.app
import common.services.authorization
import common.datatypes.domain
import common.datatypes.response
import database

import administrator.datatypes.request
import administrator.datatypes.response
import administrator.orchestrations


app = common.app.get_application()
oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="/identify/token")


@app.get(
    "/health",
    include_in_schema=False,
    response_model=common.datatypes.response.HealthCheckResponse,
)
async def health() -> common.datatypes.response.HealthCheckResponse:
    return common.datatypes.response.HealthCheckResponse(status="ok")


@app.post("/users", response_model=administrator.datatypes.response.UsersResponse)
@common.services.authorization.require_authorization(
    common.datatypes.domain.Role.ADMINISTRATOR
)
async def users(
    request: administrator.datatypes.request.UsersRequest,
    token: str = fastapi.Depends(oauth2_scheme),  # pylint: disable=unused-argument
    _database: sqlmodel.Session = fastapi.Depends(database.get_session),
) -> administrator.datatypes.response.UsersResponse:
    response = await administrator.orchestrations.arad_users(
        email_filter=request.email_filter,
        page=request.page,
        database=_database,
        user_service=None,
    )

    return administrator.datatypes.response.UsersResponse(**response)
