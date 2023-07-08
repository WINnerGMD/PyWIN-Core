from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from config import path
import requests
import re

router = APIRouter()


@router.post(f"{path}/getGJSongInfo.php", response_class=PlainTextResponse)
def get_song(songID: str = Form()):

    var = requests.get(f"https://www.newgrounds.com/audio/listen/{songID}").text


    NG_SONG_LINK = re.compile(r"(https:\\\/\\\/audio\.ngfiles\.com\\\/[^\"']+)").search(var).group(1).replace("\\/", "/")
    NG_SONG_SIZE = re.compile(r"[\"']filesize[\"'][ ]*:[ ]*(\d+)").search(var).group(1)
    NG_SONG_NAME = re.compile(r"<title>([^<>]+)</title>").search(var).group(1)
    NG_SONG_AUTH = re.compile(r"[\"']artist[\"'][ ]*:[ ]*[\"']([^\"']+)[\"']").search(var).group(1)
    print(NG_SONG_LINK)
    return f"1~|~{songID}~|~2~|~{NG_SONG_NAME}~|~3~|~2159~|~4~|~{NG_SONG_AUTH}~|~5~|~8.81~|~6~|~~|~10~|~{NG_SONG_LINK}~|~7~|~UCejLri1RVC7kj8ZVNX2a53g"
    # return "1~|~803223~|~2~|~Xtrullor - Arcana~|~3~|~2159~|~4~|~Xtrullor~|~5~|~8.81~|~6~|~~|~10~|~https%3A%2F%2Faudio.ngfiles.com%2F803000%2F803223_Xtrullor---Arcana.mp3%3Ff1524940372~|~7~|~~|~8~|~0"
    # return "1~|~1~|~2~|~Ching Cheng~|~3~|~9~|~4~|~NoName~|~5~|~8.2~|~6~|~~|~10~|~https%3A%2F%2Fdl.dropboxusercontent.com%2Fs%2F668bfemkyiali9g%2FMemealisious%2520%25E2%2580%2594%2520Ching%2520Cheng%2520Hanji%2520%2528www.lightaudio.ru%2529.mp3~|~7~|~~|~8~|~0"