import logging
from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlmodel import Session

from common.services.user import UserService
from database import get_session
from database.models import User


app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.get("/health")
async def health():
    return {"status": "healthy?"}


@app.get("/users")
async def users(
    page: int = 1,
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    user_service = UserService(database)

    user_count = await user_service.count()
    users = await user_service.list_paginated()
    pages = (user_count - 1) // 10 + 1

    return {
        "users": users,
        "count": len(users),
        "page": page,
        "pages": pages,
    }