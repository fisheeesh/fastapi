from sqlalchemy import create_engine  # type: ignore
from sqlmodel import SQLModel, Session  # type: ignore

engine = create_engine(
    url="sqlite:///sqlite.db", echo=True, connect_args={"check_same_thread": False}
)


from .models import Shipment


def creaed_db_tables():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(bind=engine) as session:
        yield session
