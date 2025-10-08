from sqlalchemy import create_engine  # type: ignore
from sqlmodel import SQLModel, Session  # type: ignore
from typing import Annotated
from fastapi import Depends # type: ignore

engine = create_engine(
    url="sqlite:///sqlite.db", echo=True, connect_args={"check_same_thread": False}
)


def creaed_db_tables():
    from .models import Shipment  # noqa: F401

    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
