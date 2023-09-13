import hashlib
from fastapi import APIRouter,Form, Depends, Request
from fastapi.responses import PlainTextResponse,  HTMLResponse
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from config import path, redis_port, redis_ttl
from services.levels import LevelService
from objects.levelObject import LevelGroup,LevelObject
from objects.schemas import GetLevel
from utils.crypt import checkValidGJP,xor_cipher,base64_encode
from utils.gdform import gd_dict_str
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer
from sqlalchemy import select
from sql import models
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
@cached(ttl=redis_ttl, cache=Cache.REDIS, key="get_levels", serializer=PickleSerializer(), port=redis_port, namespace="main")
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
              gauntlet: str = Form(default=None),
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
                      customSong=customSong,
                      gauntlet=gauntlet
                      )
    
    if gauntlet != None:
        result = await LevelService.get_gauntlets_levels(db=db, indexpack=gauntlet)
        page = 0
        is_gauntlet = True
    else:
        result = await LevelService().get_levels(db=db,data=scheme)
        page = int(page)
        is_gauntlet = False
    return await LevelGroup(service=result).GDGet_level(page=page, is_gauntlet = is_gauntlet)





@router.post(f'{path}/downloadGJLevel22.php', response_class=PlainTextResponse)
@cached(ttl=redis_ttl, cache=Cache.REDIS, key="download_levels", serializer=PickleSerializer(), port=redis_port, namespace="main")
async def level_download(levelID: str = Form(), db: AsyncSession = Depends(get_db)):
    service = await LevelService().get_level_buid(db=db,levelID=levelID)
    return await LevelObject(service=service, db=db).GDDownload_level()


@router.post(f'{path}/deleteGJLevelUser20.php', response_class=PlainTextResponse)
async def level_delete(accountID: str = Form(),
                 gjp: str = Form(),
                 levelID: str = Form(),
                   db: AsyncSession = Depends(get_db)):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        level_object = await LevelService().get_level_buid(db=db, levelID=levelID)
        if level_object.authorID == int(accountID):
            await LevelService().delete_level(db=db, levelID=levelID)
            return "1"
        
def return_hash(string):
    hash_object = hashlib.sha1(bytes(string + 'xI25fpAapCQg', 'utf-8'))
    return hash_object.hexdigest()

@router.post(f'{path}/getGJGauntlets21.php', response_class=PlainTextResponse)
async def gauntlets(db:AsyncSession = Depends(get_db)):
    gauntlets = (await db.execute(select(models.Gauntlets))).scalars().all()
    await LevelService.get_gauntlets_levels(db=db, indexpack=2)
    response = ""
    hash_string = ""
    for gn in gauntlets:
        single_response = {
            1: gn.indexpack, 3: gn.levels
        }

        hash_string += f"{gn.indexpack}{gn.levels}"
        response += gd_dict_str(single_response) + "|"

    response = response[:-1] + f"#{return_hash(hash_string)}"
    return response

@router.post(f'{path}/getGJMapPacks21.php', response_class=PlainTextResponse)
async def map_packs(page: str = Form(), db: AsyncSession = Depends(get_db)):
    packs = await LevelService.get_map_packs(db=db ,page=page)
    packstrings = []
    packhash = ""
    for pack in packs:
        packstrings.append(gd_dict_str({
            1: pack.id,
            2: pack.name,
            3: pack.levels,
            4: pack.stars,
            5: pack.coins,
            6: pack.difficulty,
            7: pack.text_color,
            8: pack.bar_color
        }))
        packhash +=(f"{str(pack.id)[0]}{str(pack.id)[-1]}{pack.stars}{pack.coins}")
    return "|".join(packstrings) + "#1:5:10#" + return_hash(packhash)
