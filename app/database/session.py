from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker  # type: ignore
from sqlmodel import SQLModel  # type: ignore
from typing import Annotated  # type: ignore
from fastapi import Depends  # type: ignore

from app.config import db_settings

engine = create_async_engine(url=db_settings.POSTGRES_URL, echo=True)


async def created_db_tables():
    async with engine.begin() as connection:
        from .models import Shipment, Seller  # noqa: F401

        await connection.run_sync(SQLModel.metadata.create_all)


# * Session to interact with database
async def get_session():
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


# * Session Dependency Annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]
