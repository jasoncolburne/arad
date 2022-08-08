from common.app import get_application
from common.datatypes.response import HealthCheckResponse


app = get_application("/api/v1/review")


@app.get("/health", include_in_schema=False, response_model=HealthCheckResponse)
async def health() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
