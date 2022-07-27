import pydantic


class HealthCheckResponse(pydantic.BaseModel):  # pylint: disable=no-member
    status: str
