from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RequestLogOut(BaseModel):
    id: int
    method: str
    endpoint: str
    partner_id: int | None
    status_code: int
    request_payload: str | None
    response_summary: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
