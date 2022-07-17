import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlmodel import Session

from common.app import get_application
from common.services.user import UserService
from database import get_session

from .types.request import UsersRequest
from .types.response import UsersResponse


app = get_application()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy?"}


@app.post("/users", response_model=UsersResponse)
async def users(
    request: UsersRequest,
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    user_service = UserService(database)
    page = request.page or 1

    return await user_service.page(number=page)
