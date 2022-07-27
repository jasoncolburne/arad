# Make sure you are editing this file in arad/core

import pydantic


class HealthCheckResponse(pydantic.BaseModel):  # pylint: disable=no-member
    status: str
