from fastapi import APIRouter  # type: ignore
from ..schemas.seller import SellerCreate, SellerRead
from ..dependencies import SellerServiceDep

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)
