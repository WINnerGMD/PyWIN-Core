import hashlib, requests, base64
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import PlainTextResponse,  HTMLResponse
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from operator import itemgetter
from config import path
from route_manager import default_route
from services.levels import LevelService
from objects.schemas import GetLevel
from helpers.security import chechValid
import json
router = APIRouter(
    prefix="",
    tags=["levels"]
)

def sha1(string):
    sha1 = hashlib.sha1()
    sha1.update(string.encode('utf-8'))
    hashed_string = sha1.hexdigest()
    return hashed_string

def levelHash(data):
    hash = ""
    for x in range(len(data)):
        hash = hash+str(data[x]["levelID"])[0]+str(data[x]["levelID"])[len(str(data[x]["levelID"]))-1]+str(data[x]["stars"])+str(data[x]["coins"])
    return sha1(hash+"xI25fpAapCQg")

@router.post(f"{path}/getGJLevels21.php", response_class=HTMLResponse)
@default_route()
async def get_level(str: str = Form(default=None),
              page: str = Form(default=None),
              type: str = Form(default=None), 
              len: str = Form(default=None),
              accountID: str = Form(default=None),
              diff: str = Form(default=None),
              demonFilter: str = Form(default=None),
              featured: str = Form(default=None),
              epic: str = Form(default=None),
              coins: str = Form(default=None),
              song: str = Form(default=None),
              customSong: str = Form(default=None),

              db: AsyncSession = Depends(get_db)):
    scheme = GetLevel(lenght=len,
                      str=str,
                      type=type,
                      accountID=accountID,
                      difficulty=diff,
                      demonFilter=demonFilter,
                      page=page,
                      featured=featured,
                      epic=epic,
                      coins=coins,
                      song=song,
                      customSong=customSong
                      )
    result = await LevelService().get_levels(db=db,data=scheme)
    levelsDataHash = []
    levelString = ""
    userString = ""
    for row in result:
        feature = 0
        epic = 0
        if row.rate == 1:
            feature = 1
        elif row.rate == 2:
            epic = 1

        levelsDataHash += [{"levelID":row.id,"stars":row.stars,"coins":row.user_coins}]
        levelString += f'1:{row.id}:2:{row.name}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{feature}:42:{epic}:45:{row.objects}:3:{row.desc}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:37:{row.coins}:38:{row.user_coins}:39:{0}:46:1:47:2:35:{row.song_id}|'

        userString += f'{row.authorID}:{row.authorName}:{row.authorID}|'
    return f"{levelString}#{userString}##{2}:{int(page+'0')}:5#{levelHash(levelsDataHash)}"


def downloadLevelHash1(levelString):
    hash = ""
    dataLen = len(levelString)
    divided = int(dataLen/40)
    p = 0
    k = 0
    while k < dataLen:
        if p > 39: break
        hash += levelString[k]
        p+=1
        k = k + divided
    return sha1(hash+"xI25fpAapCQg")

def downloadLevelHash2(levelData):
    return sha1(levelData+"xI25fpAapCQg")

def base64_encode(string):
    return base64.b64encode(str(string).encode("utf-8")).decode("utf-8")

def xor_cipher(text, key):
    # потом перепишу с php на py
    return requests.get(f"https://xor-cipher.dimluxdev.repl.co/?text={text}&key={key}").text

@router.post(f'{path}/downloadGJLevel22.php', response_class=PlainTextResponse)
@default_route()
async def level_download(levelID: str = Form(), db: AsyncSession = Depends(get_db)):
    if levelID != "-1":
        row = await LevelService().get_level_buid(db=db,levelID=levelID)
        return f'1:{row.id}:2:{row.name}:3:{row.desc}:4:{row.LevelString}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{"1" if row.rate == 1 else "0"}:42:{"1" if row.rate == 2 else "0"}:45:{row.objects}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:28:{0}:29:{0}:35:{row.song_id}:36::37:{row.coins}:38:{row.user_coins}:39:{0}:46::47::40:{row.is_ldm}:27:{base64_encode(xor_cipher(row.password, 26364))}#{downloadLevelHash1(row.LevelString)}#' + downloadLevelHash2(f'{row.authorID},{row.stars},{0},{row.id},{row.user_coins},{"1" if row.rate == 1 else "0"},{row.password},0')
    else:
        print(levelID)
        row = await LevelService().get_level_buid(db=db,levelID=17)
        return f'1:{row.id}:2:{row.name}:3:{row.desc}:4:{row.LevelString}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{"1" if row.rate == 1 else "0"}:42:{"1" if row.rate == 2 else "0"}:45:{row.objects}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:28:{0}:29:{0}:35:{row.song_id}:36::37:{row.coins}:38:{row.user_coins}:39:{0}:46::47::40:{row.is_ldm}:27:{base64_encode(xor_cipher(row.password, 26364))}#{downloadLevelHash1(row.LevelString)}#' + downloadLevelHash2(f'{row.authorID},{row.stars},{0},{row.id},{row.user_coins},{"1" if row.rate == 1 else "0"},{row.password},0')


@router.post(f'{path}/deleteGJLevelUser20.php', response_class=PlainTextResponse)
async def level_delete(accountID: str = Form(),
                 gjp: str = Form(),
                 levelID: str = Form(),
                   db: AsyncSession = Depends(get_db)):
    if await chechValid(id=accountID, gjp=gjp, db=db):
        level_object = await LevelService().get_level_buid(db=db, level_id=levelID)
        if level_object.authorID == int(accountID):
            await LevelService().delete_level(db=db, levelID=levelID)
            return "1"
