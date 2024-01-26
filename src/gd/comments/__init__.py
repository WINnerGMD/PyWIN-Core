from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from . import posts, comments


def init_routers(router: APIRouter) -> None:
    router.include_router(comments.router)
    router.include_router(posts.router)


def init_comments() -> APIRouter:
    router = APIRouter(default_response_class=PlainTextResponse)
    init_routers(router)
    return router
