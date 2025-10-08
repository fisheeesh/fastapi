from sqlalchemy import create_engine  # type: ignore
from sqlmodel import SQLModel  # type: ignore

engine = create_engine(
    url="sqlite:///sqlite.db", echo=True, connect_args={"check_same_thread": False}
)


def creaed_db_tables():
    from .models import Shipment
    SQLModel.metadata.create_all(bind=engine)
