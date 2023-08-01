from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from config import path
import requests
import re
# from database import db
from route_manager import default_route

router = APIRouter()


@router.post(f"{path}/getGJSongInfo.php", response_class=PlainTextResponse)
@default_route()
def get_song(songID: str = Form()):
    # songItem = db(f"SELECT * FROM songs WHERE `songid` = '{songID}'")
    # print(songItem)
    # if songItem != []:
    #     link = songItem[0]["link"]
    #     name = songItem[0]["name"]
    #     author = songItem[0]["author"]

    # else:
    var = requests.get(f"https://www.newgrounds.com/audio/listen/{songID}").text
    link = re.compile(r"(https:\\\/\\\/audio\.ngfiles\.com\\\/[^\"']+)").search(var).group(1).replace("\\/", "/")
    # size = re.compile(r"[\"']filesize[\"'][ ]*:[ ]*(\d+)").search(var).group(1)
    name = re.compile(r"<title>([^<>]+)</title>").search(var).group(1)
    author = re.compile(r"[\"']artist[\"'][ ]*:[ ]*[\"']([^\"']+)[\"']").search(var).group(1)
    # db(f"INSERT INTO `songs`(`songid`, `link`, `name`, `author`) VALUES ('{songID}','{link}','{name}','{author}')")
    return f"1~|~{songID}~|~2~|~{name}~|~3~|~2159~|~4~|~{author}~|~5~|~8.81~|~6~|~~|~10~|~{link}~|~7~|~UCejLri1RVC7kj8ZVNX2a53g"

    # return "1~|~803223~|~2~|~Xtrullor - Arcana~|~3~|~2159~|~4~|~Xtrullor~|~5~|~8.81~|~6~|~~|~10~|~https%3A%2F%2Faudio.ngfiles.com%2F803000%2F803223_Xtrullor---Arcana.mp3%3Ff1524940372~|~7~|~~|~8~|~0"
    # return "1~|~1~|~2~|~Ching Cheng~|~3~|~9~|~4~|~NoName~|~5~|~8.2~|~6~|~~|~10~|~https%3A%2F%2Fdl.dropboxusercontent.com%2Fs%2F668bfemkyiali9g%2FMemealisious%2520%25E2%2580%2594%2520Ching%2520Cheng%2520Hanji%2520%2528www.lightaudio.ru%2529.mp3~|~7~|~~|~8~|~0"