# Make sure you are editing this file in arad/core

import logging
import os
import typing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import common.current_user_cache

DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT")
LOCAL = DEPLOYMENT_ENVIRONMENT == "development"


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args[2] != "/health"  # type: ignore


logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

old_factory = logging.getLogRecordFactory()


def record_factory(*args: typing.Any, **kwargs: typing.Any) -> logging.LogRecord:
    record = old_factory(*args, **kwargs)
    record.user_id = common.current_user_cache.application_cache.get_current_user_id()
    return record


logging.setLogRecordFactory(record_factory)


def get_application(root_path: str) -> FastAPI:
    app = FastAPI(
        openapi_url="/openapi.json" if LOCAL else None,
        docs_url="/docs" if LOCAL else None,
        redoc_url=None,
        root_path=root_path,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.environ["ALLOWED_ORIGINS"].split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
