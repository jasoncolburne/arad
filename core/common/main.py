# Make sure you are editing this file in arad/core

import os
import toml
import uvicorn


DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT", "production")
LISTEN_IP = os.environ.get("LISTEN_IP", "127.0.0.1")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "80"))
LOCAL = DEPLOYMENT_ENVIRONMENT == "development"


def start() -> None:
    """Launched with `poetry run start` at root level"""
    project = toml.load("pyproject.toml")
    module = project["tool"]["poetry"]["name"]
    entrypoint = f"{module}.app:app"
    uvicorn.run(entrypoint, host=LISTEN_IP, port=LISTEN_PORT, reload=LOCAL)
