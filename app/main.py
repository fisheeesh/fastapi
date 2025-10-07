from fastapi import FastAPI  # type: ignore
from scalar_fastapi import get_scalar_api_reference  # type: ignore
from typing import Any

app = FastAPI()


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    return {"id": id, "weight": 1.2, "content": "wooden table", "status": "in transit"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
