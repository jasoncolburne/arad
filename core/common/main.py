# Make sure you are editing this file in arad/core

import os
import toml
import uvicorn


DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT", "production")
LISTEN_IP = os.environ.get("LISTEN_IP", "127.0.0.1")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "80"))
LOCAL = DEPLOYMENT_ENVIRONMENT == "development"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(asctime)s %(levelprefix)-9s [%(name)s] %(message)s",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "format": '%(asctime)s %(levelprefix)-9s [%(name)s] %(client_addr)s "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["default"],
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["access"],
        },
    },
}


def start() -> None:
    """Launched with `poetry run start` at root level"""
    project = toml.load("pyproject.toml")
    module = project["tool"]["poetry"]["name"]
    entrypoint = f"{module}.app:app"
    uvicorn.run(
        entrypoint,
        host=LISTEN_IP,
        port=LISTEN_PORT,
        reload=LOCAL,
        log_config=LOGGING_CONFIG,
    )
