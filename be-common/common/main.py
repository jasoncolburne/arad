import os
import toml
import uvicorn


ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT")

def start():
    """Launched with `poetry run start` at root level"""
    project = toml.load("pyproject.toml")
    module = project["tool"]["poetry"]["name"]
    uvicorn.run(f"{module}.app:app", host="0.0.0.0", port=80, reload=(ENVIRONMENT == "development"))
