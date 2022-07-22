from fastapi import FastAPI


app = FastAPI()

@app.middleware("errors")
async def handle_errors(request: Request, call_next):
    try:
        return await call_next(request)
    except (ex):
        log.error(request, ex)
        raise HttpException(code=500, message="Internal server error")
