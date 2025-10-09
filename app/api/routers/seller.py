from fastapi import APIRouter, Depends, HTTPException, status

from app.uitls import decode_access_token  # type: ignore
from ..schemas.seller import SellerCreate, SellerRead
from ..dependencies import SellerServiceDep
from fastapi.security import OAuth2PasswordRequestForm  # type: ignore
from typing import Annotated
from app.core.security import oauth2_scheme

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


@router.get("/dashboard")
async def get_dashboard(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    return {
        "detail": "Successfully Authenticated",
    }
