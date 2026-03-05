from pydantic import BaseModel, ConfigDict


class PartnerBase(BaseModel):
    name: str
    rate_limit_per_minute: int = 60


class PartnerCreate(PartnerBase):
    pass


class PartnerOut(PartnerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PartnerCreateResponse(PartnerOut):
    api_key: str
