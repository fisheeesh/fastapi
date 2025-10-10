from fastapi import APIRouter, Depends

from app.database.redis import add_jti_to_blacklist

from ..schemas.seller import SellerCreate, SellerRead
from ..dependencies import SellerServiceDep, get_access_token
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from typing import Annotated

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)

    return {
        "access_token": token,
        "type": "jwt",
    }


@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}
