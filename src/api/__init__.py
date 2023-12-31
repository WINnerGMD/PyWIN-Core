from fastapi import FastAPI
from .levels.get_levels import router as get_levels
from .users.get_users import router as get_users


def init_routers(api: FastAPI) -> None:
    """Initial all routers of JSON:API"""
    api.include_router(get_levels)
    api.include_router(get_users)


def init_api() -> FastAPI:
    api = FastAPI(
        title="PyWIN Core API Doc",
        docs_url="/swagger",
        version='2.0'
    )
    init_routers(api)
    return api
