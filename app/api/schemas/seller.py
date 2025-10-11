from pydantic import BaseModel, EmailStr  # type: ignore


class BaseSeller(BaseModel):
    name: str
    email: EmailStr
    address: str
    zip_code: int


class SellerRead(BaseSeller):
    pass


class SellerCreate(BaseSeller):
    password: str
