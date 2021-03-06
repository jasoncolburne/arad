import os
import toml
import uvicorn


DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT")
LISTEN_IP = os.environ.get("LISTEN_IP", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "80"))
LOCAL = DEPLOYMENT_ENVIRONMENT == "development"


def start() -> None:
    """Launched with `poetry run start` at root level"""
    project = toml.load("pyproject.toml")
    module = project["tool"]["poetry"]["name"]
    entrypoint = f"{module}.app:app"
    uvicorn.run(entrypoint, host=LISTEN_IP, port=LISTEN_PORT, reload=LOCAL)
