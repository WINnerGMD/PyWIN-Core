from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from . import management, page, auth


router = APIRouter(default_response_class=PlainTextResponse)


router.include_router(auth.router)
router.include_router(management.router)
router.include_router(page.router)
