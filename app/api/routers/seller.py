from fastapi import APIRouter, Depends  # type: ignore
from ..schemas.seller import SellerCreate, SellerRead
from ..dependencies import SellerServiceDep
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from typing import Annotated

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/token")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    request_form.password
