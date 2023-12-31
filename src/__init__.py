from fastapi import FastAPI
from .api import init_api
from .gd import init_gd


def init_apis(app: FastAPI) -> None:
    app.mount("/winnertestss", init_gd())
    app.mount("/v2", init_api())


def init_app() -> FastAPI:
    app = FastAPI(
        docs_url=None
    )

    init_apis(app)
    return app
