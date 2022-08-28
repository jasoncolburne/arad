# Make sure you are editing this file in arad/core

import os
import toml
import uvicorn


DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT", "production")
LISTEN_IP = os.environ.get("LISTEN_IP", "127.0.0.1")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "80"))
LOCAL = DEPLOYMENT_ENVIRONMENT == "development"

JOB_NAME = os.environ.get("NOMAD_JOB_NAME", "service")
SHORT_ALLOC_ID = os.environ.get("NOMAD_SHORT_ALLOC_ID", "ffffffff")
DATACENTER = os.environ.get("NOMAD_DC", "dc1")
TASK_NAME = os.environ.get("NOMAD_TASK_NAME", "fastapi")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": f"%(asctime)s %(levelprefix)-9s [{DATACENTER}|{JOB_NAME}|{SHORT_ALLOC_ID}|%(name)s|{TASK_NAME}|%(module)s] %(message)s",  # pylint: disable=line-too-long
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "format": f'%(asctime)s %(levelprefix)-9s [{DATACENTER}|{JOB_NAME}|{SHORT_ALLOC_ID}|%(name)s|{TASK_NAME}] %(client_addr)s "%(request_line)s" %(status_code)s',  # pylint: disable=line-too-long
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
