from fastapi import FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate
from .database import shipments, save

app = FastAPI()

# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@app.get("/shipment", response_model=None)
def get_shipment_by_id(id: int):
    # if not id:
    #     id = max(shipments.keys())
    #     return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipments[id]


# * Accept with body
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed",
    }
    save()
    return {"id": new_id}


# * with body
@app.patch("/shipment", response_model=ShipmentRead)
def patch_shipment(id: int, body: ShipmentUpdate):
    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
