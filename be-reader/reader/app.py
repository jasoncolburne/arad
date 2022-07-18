from common.app import get_application


app = get_application()


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "healthy?"}
