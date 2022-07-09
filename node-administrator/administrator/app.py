from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlmodel import Session

from database import get_session
from database.models import User

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://arad.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users", response_model=list[User])
async def users(session: Session = Depends(get_session)):
    query = await session.execute(select(User))
    return query.scalars().all()
