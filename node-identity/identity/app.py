from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlmodel import Session

from database import get_session
from database.models import User

from fastapi.middleware.cors import CORSMiddleware


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


@app.get("/health")
async def health():
    return


@app.post("/register", response_model=User)
async def register(body: dict, session: Session = Depends(get_session)):
    user = User(email=body['email'])
    session.add(user)
    await session.commit()
    return user
