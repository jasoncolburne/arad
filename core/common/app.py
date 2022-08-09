# Make sure you are editing this file in arad/core

import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT")
LOCAL = DEPLOYMENT_ENVIRONMENT == "development"


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args[2] != "/health"  # type: ignore


logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


def get_application(root_path: str) -> FastAPI:
    app = FastAPI(
        openapi_url="/openapi.json" if LOCAL else None,
        docs_url="/docs" if LOCAL else None,
        redoc_url=None,
        root_path=root_path,
    )

    origins = os.environ["ALLOWED_ORIGINS"].split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
