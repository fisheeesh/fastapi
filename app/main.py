from fastapi import FastAPI # pyright: ignore[reportMissingImports]

app = FastAPI()

@app.get("/shipment")
def get_shipment():
    return {
        "content" : "wooden table",
        "status": "in transit"
    }