# from fastapi import APIRouter, Form, Depends
# from fastapi.responses import PlainTextResponse
# from config import path
# import requests
# import re
# from database import get_db
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sql import models
# from route_manager import default_route

# router = APIRouter()


# @router.post(f"{path}/getGJSongInfo.php", response_class=PlainTextResponse)
# @default_route()
# async def get_song(songID: str = Form(), db: AsyncSession = Depends(get_db)):
#     song_db = (await db.execute(select(models.Songs).filter(models.Songs.song_id == songID))).scalars().first()
#     print(song_db)
#     if song_db == None:
#         var = requests.get(f"https://www.newgrounds.com/audio/listen/{songID}").text
#         link = re.compile(r"(https:\\\/\\\/audio\.ngfiles\.com\\\/[^\"']+)").search(var).group(1).replace("\\/", "/")
#         size = int(re.compile(r"[\"']filesize[\"'][ ]*:[ ]*(\d+)").search(var).group(1)) / 1024**2
#         name = re.compile(r"<title>([^<>]+)</title>").search(var).group(1)
#         author = re.compile(r"[\"']artist[\"'][ ]*:[ ]*[\"']([^\"']+)[\"']").search(var).group(1)


#         new_song = models.Songs(song_id = songID, name = name, author = author, link = link, size=size)
#         db.add(new_song)
#         await db.commit()
#         await db.refresh(new_song)
#     else:
#         songID = song_db.song_id
#         name = song_db.name
#         author = song_db.author
#         size = song_db.size
#         link = song_db.link
#     return f"1~|~{songID}~|~2~|~{name}~|~3~|~2159~|~4~|~{author}~|~5~|~{size}~|~6~|~~|~10~|~{link}~|~7~|~UCejLri1RVC7kj8ZVNX2a53g"

#     # return "1~|~803223~|~2~|~Xtrullor - Arcana~|~3~|~2159~|~4~|~Xtrullor~|~5~|~8.81~|~6~|~~|~10~|~https%3A%2F%2Faudio.ngfiles.com%2F803000%2F803223_Xtrullor---Arcana.mp3%3Ff1524940372~|~7~|~~|~8~|~0"
#     # return "1~|~1~|~2~|~Ching Cheng~|~3~|~9~|~4~|~NoName~|~5~|~8.2~|~6~|~~|~10~|~https%3A%2F%2Fdl.dropboxusercontent.com%2Fs%2F668bfemkyiali9g%2FMemealisious%2520%25E2%2580%2594%2520Ching%2520Cheng%2520Hanji%2520%2528www.lightaudio.ru%2529.mp3~|~7~|~~|~8~|~0"



import requests
import re

id = input('введи айди')
var = requests.get(f"https://www.newgrounds.com/audio/listen/{id}").text
link = re.compile(r"(https:\\\/\\\/audio\.ngfiles\.com\\\/[^\"']+)").search(var).group(1).replace("\\/", "/")
size = int(re.compile(r"[\"']filesize[\"'][ ]*:[ ]*(\d+)").search(var).group(1)) / 1024**2
name = re.compile(r"<title>([^<>]+)</title>").search(var).group(1)
author = re.compile(r"[\"']artist[\"'][ ]*:[ ]*[\"']([^\"']+)[\"']").search(var).group(1)
print(link)