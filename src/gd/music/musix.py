from typing import Annotated

from fastapi import APIRouter, Form, Depends, Header, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from src.models import SongsModel

# with open('/gd/music/musix_config.json', 'r') as f:
#     config = json.loads(f.read())

SECRET = "secret"

router = APIRouter(tags=["Songs"])

@router.post(f"{system.path}/getCustomContentURL.php",response_class=PlainTextResponse)
async def get_song(req: Request):
    print(await req.form())
    return "https://geometrydashfiles.b-cdn.net/"

@router.post(f"/getGJSongInfo.php", response_class=PlainTextResponse)
async def get_song(songID: str = Form()):
    if songID == "100000":
        name = "Noko Shikanoko"
        author = "Shikairo Days"
        link = "https://uznavo.com/files/mp3/rus-mp3/shikairo-days-noko-shikanoko.mp3"
        size = 7.79
        return f"1~|~{songID}~|~2~|~{name}~|~3~|~2159~|~4~|~{author}~|~5~|~{size}~|~6~|~~|~10~|~{link}~|~7~|~UCejLri1RVC7kj8ZVNX2a53g"


