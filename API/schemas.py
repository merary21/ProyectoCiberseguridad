from pydantic import BaseModel, Field


class WebRequest(BaseModel):
    method: str = Field(..., min_length=1)
    url: str = Field(..., min_length=1)
    status_code: int = Field(..., ge=100, le=599)
    response_size: int = Field(..., ge=0)
    user_agent: str = Field(..., min_length=1)
    ip: str = Field(..., min_length=1)