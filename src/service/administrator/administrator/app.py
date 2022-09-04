import common.app
import common.datatypes.response

app = common.app.get_application("/api/v1/administrate")


@app.get(
    "/health",
    include_in_schema=False,
    response_model=common.datatypes.response.HealthCheckResponse,
)
async def health() -> common.datatypes.response.HealthCheckResponse:
    return common.datatypes.response.HealthCheckResponse(status="ok")
