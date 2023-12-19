from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import database

SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{database.user}:{database.password}@{database.host}/{database.database}"
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{database.user}:{database.password}@db/{database.database}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


