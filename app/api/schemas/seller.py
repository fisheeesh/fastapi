from pydantic import BaseModel, EmailStr  # type: ignore


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
