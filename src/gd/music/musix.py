from typing import Annotated

from fastapi import APIRouter, Form, Depends, Header
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from database import get_db
from models import SongsModel

# with open('/gd/music/musix_config.json', 'r') as f:
#     config = json.loads(f.read())

SECRET = "secret"

router = APIRouter(tags=["Songs"])


@router.post(f"{system.path}/getGJSongInfo.php", response_class=PlainTextResponse)
async def get_song(songID: str = Form(), db: AsyncSession = Depends(get_db)):
    song_db = (
        (await db.execute(select(SongsModel).filter(SongsModel.id == songID)))
        .scalars()
        .first()
    )

    if song_db is not None:
        songID = song_db.id
        name = song_db.name
        author = song_db.author
        size = song_db.size
        link = song_db.link
        if "musix:" in song_db.link:
            if "yt" in song_db.link:
                print(song_db.link)
                musixID = song_db.link.split(":")[-1].split("-")[-1]
                print(musixID)
                link = f"http://95.163.240.218/data/{musixID}.mp3"

                print(link)

        return f"1~|~{songID}~|~2~|~{name}~|~3~|~2159~|~4~|~{author}~|~5~|~{size}~|~6~|~~|~10~|~{link}~|~7~|~UCejLri1RVC7kj8ZVNX2a53g"


class get_musix(BaseModel):
    status: str
    type: str
    name: str
    author: str
    size: float
    link: str


@router.post("/musix")
async def musix_get(
    data: get_musix,
    Authorization: Annotated[str, Header()],
    db: AsyncSession = Depends(get_db),
):
    global song_link
    try:
        if Authorization == SECRET:
            if data.type == "yt":
                song_link = f"musix:yt-{data.link}"
            elif data.type == "ng":
                song_link = data.link
            db_model = SongsModel(
                name=data.name, author=data.author, size=data.size, link=song_link
            )
            db.add(db_model)
            await db.commit()
            await db.refresh(db_model)
            return {"status": "ok", "id": db_model.id}
        else:
            print("error 2")
            return {"status": "error"}
    except Exception as ex:
        print(ex)
        return {"status": "error"}


# class setup_musix(BaseModel):

# @router.post('/musix/setup')
# async def setup_musix():
