import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT")

def get_application():
    app = FastAPI(
        openapi_url="/openapi.json" if ENVIRONMENT == "development" else None,
        docs_url="/docs" if ENVIRONMENT == "development" else None,
        redoc_url=None,   
    )

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

    return app
