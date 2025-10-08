from fastapi import APIRouter  # type: ignore
from ..schemas.seller import SellerCreate

router = APIRouter(prefix="/seller")


@router.post("/signup")
def register_seller(seller: SellerCreate):
    pass
