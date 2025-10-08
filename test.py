from fastapi import FastAPI  # type: ignore
from contextlib import asynccontextmanager

from rich import print, panel # type: ignore


@asynccontextmanager
async def lifespan_hanlder(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    yield
    print(panel.Panel("...stopped!", border_style="red"))


app = FastAPI(lifespan=lifespan_hanlder)


@app.get("/")
def read_root():
    return {"detail": "Server running..."}
