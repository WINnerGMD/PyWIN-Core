from fastapi import FastAPI
from .api import init_api
from .gd import init_gd
from database import Base, engine
import asyncio


def init_migrations(app: FastAPI) -> None:

    @app.on_event("startup")
    async def on_startup() -> None:
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all) if you need clear all data
            await conn.run_sync(Base.metadata.create_all)


def init_apis(app: FastAPI) -> None:
    app.mount("/winnertestss", init_gd())
    app.mount("/v2", init_api())


def init_app() -> FastAPI:
    app = FastAPI(
        docs_url=None
    )
    init_migrations(app)
    init_apis(app)
    return app
