import os
import toml
import uvicorn


DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT")

def start():
    """Launched with `poetry run start` at root level"""
    project = toml.load("pyproject.toml")
    module = project["tool"]["poetry"]["name"]
    local = DEPLOYMENT_ENVIRONMENT == "development"
    uvicorn.run(f"{module}.app:app", host="0.0.0.0", port=(8000 if local else 80), reload=local)
