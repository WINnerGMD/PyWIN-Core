from fastapi import FastAPI

from .accounts import init_accounts
from .comments import init_comments
from .levels import router as router_levels
from .misc.likes import router as router_likes
from .music.musix import router as router_music
from .rewards.chest import router as router_chest
from .lists.lists import router as router_lists
from .scores.scores import router as router_scores


def init_routers(gd: FastAPI) -> None:
    gd.include_router(init_accounts())
    gd.include_router(router_levels)
    gd.include_router(init_comments())
    gd.include_router(router_likes)
    gd.include_router(router_music)
    gd.include_router(router_scores)
    # gd.include_router(router_rate)
    gd.include_router(router_chest)
    gd.include_router(router_lists)


def init_gd() -> FastAPI:
    gd = FastAPI(
        docs_url=f"/swagger",
        redoc_url=None,
        title="PyWIN Core",
        summary="For developers and testers",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    )

    init_routers(gd)
    return gd
