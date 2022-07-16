from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import exc
from sqlmodel import Session

from common.services.role import RoleService
from common.services.user import UserService
from identity.services.authentication import AuthenticationService

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

@app.get("/health")
async def health():
    return {"status": "healthy?"}


# endpoints can share this since it is stateless
authentication_service = AuthenticationService()

@app.post("/register")
async def register(body: dict, database: Session = Depends(get_session)):
    email = body['email']
    passphrase = body['passphrase']
    
    hashed_passphrase = authentication_service.hash_passphrase(passphrase)
    user = User(email=email, hashed_passphrase=hashed_passphrase)

    user_service = UserService(database)
    try:
        await user_service.create(user)
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email address",
        )

    role_service = RoleService()
    roles = role_service.list_current(user)
    access_token = authentication_service.create_access_token(user)
    return {
        "credentials": {"token": access_token, "token_type": "bearer"},
        "user": {"id": user.id, "email": user.email},
        "roles": roles,
    }


@app.post("/login")
async def login(body: dict, database: Session = Depends(get_session)):
    authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = body['email']
    passphrase = body['passphrase']

    user_service = UserService(database)
    try:
        user = await user_service.get_by_email(email)
    except exc.NoResultFound:
        raise authentication_exception

    if not authentication_service.authenticate_user(user, passphrase):
        raise authentication_exception

    role_service = RoleService()
    roles = role_service.list_current(user)
    access_token = authentication_service.create_access_token(user)
    return {
        "credentials": {"token": access_token, "token_type": "bearer"},
        "user": {"id": user.id, "email": user.email},
        "roles": roles,
    }
