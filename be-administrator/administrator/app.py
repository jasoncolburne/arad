from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from common.app import get_application
from common.services.authorization import require_authorization
from common.datatypes.response import Role
from database import get_session

from .datatypes.request import UsersRequest
from .datatypes.response import UsersResponse
from .orchestrations import arad_users


app = get_application()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/identify/token")


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy?"}


@app.post("/users", response_model=UsersResponse)
@require_authorization(Role.ADMINISTRATOR)
async def users(
    request: UsersRequest,
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    return await arad_users(
        email_filter=request.email_filter, page=request.page, database=database
    )
