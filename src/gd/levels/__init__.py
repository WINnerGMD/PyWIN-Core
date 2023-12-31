from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from . import level_packs, levels


router = APIRouter(default_response_class=PlainTextResponse)


router.include_router(levels.router)
router.include_router(level_packs.router)
