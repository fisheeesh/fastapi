from fastapi import FastAPI, HTTPException, status  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore
from typing import Any

app = FastAPI()

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


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())

    return shipments[id]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        return {"details": "Given id doesn't exit!"}

    return shipments[id]


# * in fastapi accepting query para, it is enough just pass the qPara in route handle func
@app.get("/shipments")
def get_shipment_by_id(id: int) -> dict[str, Any]:
    if not id:
        id = max(shipments.keys())
        return shipments[id]

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!"
        )

    return shipments[id]


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
