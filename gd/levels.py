from fastapi import APIRouter, Request,Form
from fastapi.responses import PlainTextResponse
router = APIRouter(
    prefix="",
    tags=["levels"]
)

@router.post("/winnertests/getGJLevels21.php", response_class=PlainTextResponse)
async def get_level():    
    return ":1:2:2:"
