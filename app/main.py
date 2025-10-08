from fastapi import FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore
from typing import Any

from pydantic import BaseModel  # type: ignore

app = FastAPI()


class Shipment(BaseModel):
    content: str
    weight: float
    destination: int
    status: str


shipments = {
    162002: {
        "weight": 0.6,
        "content": "glassware",
        "status": "placed",
    },
    162003: {
        "weight": 2.3,
        "content": "electronics",
        "status": "shipped",
    },
    162004: {
        "weight": 1.5,
        "content": "books",
        "status": "delivered",
    },
    162005: {
        "weight": 0.8,
        "content": "clothing",
        "status": "processing",
    },
    162006: {
        "weight": 3.2,
        "content": "furniture",
        "status": "placed",
    },
    162007: {
        "weight": 0.4,
        "content": "cosmetics",
        "status": "shipped",
    },
    162008: {
        "weight": 5.7,
        "content": "sports equipment",
        "status": "cancelled",
    },
}


# * order matters
@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    return shipments[id][field]


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())

    return shipments[id]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        return {"details": "Given id doesn't exit!"}

    return shipments[id]


# * In fastapi accepting query para, it is enough just pass the qPara in route handle func
@app.get("/shipment")
def get_shipment_by_id(id: int) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipments[id]


# * Accept with query params
# @app.post("/shipment")
# def submit_shipment(content: str, weight: float) -> dict[str, int]:
#     if weight > 25:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail="Maximum weight limit is 25 kgs",
#         )

#     new_id = max(shipments.keys()) + 1

#     shipments[new_id] = {"content": content, "weight": weight, "status": "placed"}
#     return {"id": new_id}


# * Accept with body
@app.post("/shipment")
def submit_shipment(body: Shipment) -> dict[str, int]:
    if body.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximun weight limit is 25 kgs",
        )

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {"content": body.content, "weight": body.weight, "status": body.status}
    return {"id": new_id}


@app.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, statuss: str
) -> dict[str, Any]:
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximun weight limit is 25 kgs",
        )

    shipments[id] = {"content": content, "weight": weight, "status": statuss}

    return shipments[id]


# * with query params
# @app.patch("/shipment")
# def patch_shipment(
#     id: int,
#     content: str | None = None,
#     weight: float | None = None,
#     statuss: str | None = None,
# ) -> dict[str, Any]:
#     if weight is not None and weight > 25:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail="Maximun weight limit is 25 kgs",
#         )

#     shipment = shipments[id]
#     if content:
#         shipment["content"] = content
#     elif weight:
#         shipment["weight"] = weight
#     if statuss:
#         shipment["status"] = statuss

#     shipments[id] = shipment

#     return shipments[id]


# * with body
@app.patch("/shipment")
def patch_shipment(id: int, body: dict[str, Any]) -> dict[str, Any]:
    # weight = body["weight"]

    # if weight > 25:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #         detail="Maximun weight limit is 25 kgs",
    #     )

    shipment = shipments[id]

    shipment.update(body)

    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
