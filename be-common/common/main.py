import toml
import uvicorn


def start():
    """Launched with `poetry run start` at root level"""
    project = toml.load("pyproject.toml")
    module = project["tool"]["poetry"]["name"]
    uvicorn.run(f"{module}.app:app", host="0.0.0.0", port=8000, reload=True)
