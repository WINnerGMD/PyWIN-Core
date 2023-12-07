from fastapi import APIRouter
from . import management, page, auth


router = APIRouter()


router.include_router(auth.router)
router.include_router(management.router)
router.include_router(page.router)
