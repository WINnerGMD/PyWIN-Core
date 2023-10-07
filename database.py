from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import database

SQLALCHEMY_DATABASE_URL = f'mysql+aiomysql://{database.user}:{database.password}@{database.host}/{database.database}'
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://habrpguser:pgpwd4habr@pgdatabase/habrdb"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()


async def get_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    except Exception:
        ...

    try:
        db = SessionLocal(expire_on_commit=True)
        yield db
    finally:
        await db.close()
