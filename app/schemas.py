from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class PartnerBase(BaseModel):
    name: str
    rate_limit_per_minute: int = 60


class PartnerCreate(PartnerBase):
    pass


class PartnerOut(PartnerBase):
    id: int
    api_key: str

    class Config:
        from_attributes = True