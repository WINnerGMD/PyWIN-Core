from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api import init_api
from .gd import init_gd
from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def init_apis(app: FastAPI) -> None:
    app.mount("/winnertestss", init_gd())
    app.mount("/v2", init_api())


def init_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        lifespan=lifespan
    )
    init_apis(app)
    return app

