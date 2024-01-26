from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from . import management, page, auth


def init_routers(router: APIRouter) -> None:
    router.include_router(auth.router)
    router.include_router(management.router)
    router.include_router(page.router)


def init_accounts() -> APIRouter:
    router = APIRouter(default_response_class=PlainTextResponse)
    init_routers(router)
    return router
