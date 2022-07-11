import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select
from sqlmodel import Session

from database import get_session
from database.models import User


app = FastAPI()

origins = [
    "http://arad.org",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/health")
async def health():
    return {"status": "healthy?"}


@app.get("/users", response_model=list[User])
async def users(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    query = await session.execute(select(User))
    return query.scalars().all()
