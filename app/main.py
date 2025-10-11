from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.database.session import created_db_tables

from fastapi import BackgroundTasks, FastAPI  # type: ignore

from app.api.router import master_router
from app.services.notificatoin import NotificationService


@asynccontextmanager
async def lifespan_hanlder(app: FastAPI):
    await created_db_tables()
    yield


app = FastAPI(lifespan=lifespan_hanlder)

app.include_router(master_router)


@app.get("/mail")
async def send_test_email(tasks: BackgroundTasks):
    tasks.add_task(
        NotificationService().send_email,
        recipients=["yavut@mailto.plus"],
        subject="Test Mail Coming Through Once",
        body="You shouldn't be interested in every body...",
    )

    return {"detail": "Sending mail..."}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
