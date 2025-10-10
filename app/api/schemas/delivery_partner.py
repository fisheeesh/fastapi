from pydantic import BaseModel, EmailStr  # type: ignore
from sqlmodel import Field  # type: ignore


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseDeliveryPartner):
    pass


class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str


class DeliveryPartnerUpdate(BaseModel):
    serviceable_zip_codes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)
