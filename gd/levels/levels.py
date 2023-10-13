import hashlib
from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from config import system, redis
from services.levels import LevelService
from objects.levelObject import LevelGroup, LevelObject
from objects.schemas import GetLevel, UploadLevel
from utils.crypt import checkValidGJP
from utils.gdform import gd_dict_str
from cache import cache
from sqlalchemy import select
from sql import models
from logger import info, error
import json
from helpers.rate import Difficulty

router = APIRouter(prefix="", tags=["Levels"])


@router.post(f"{system.path}/uploadGJLevel21.php")
async def upload_level(
        db: AsyncSession = Depends(get_db),
        levelString: str = Form(),
        accountID: int = Form(),
        levelName: str = Form(),
        levelDesc: str = Form(default="WyBoZXkgaGUgZGlkbid0IHB1dCBhIGRlc2NyaXB0aW9uIF0="),
        levelVersion: int = Form(),
        levelLength: int = Form(),
        audioTrack: int = Form(),
        password: int = Form(),
        original: int = Form(),
        twoPlayer: int = Form(),
        songID: int = Form(),
        objects: int = Form(),
        coins: int = Form(),
        requestedStars: int = Form(),
        ldm: int = Form(),
        gameVersion: int = Form(),
        gjp: str = Form()
):
    if await checkValidGJP(accountID, gjp=gjp, db=db):
        SystemObj = UploadLevel(
            levelString=levelString,
            accountID=accountID,
            levelName=levelName,
            levelDesc=levelDesc,
            levelVersion=levelVersion,
            levelLength=levelLength,
            audioTrack=audioTrack,
            password=password,
            original=original,
            twoPlayer=twoPlayer,
            songID=songID,
            objects=objects,
            coins=coins,
            requestedStars=requestedStars,
            ldm=ldm,
            gameVersion=gameVersion,
        )
        service = await LevelService().upload_level(db=db, data=SystemObj)
        print(service)
        if service['status'] == 'ok':
            return service['level'].id
        else:
            error(service['details'])
            return "-1"


@router.post(f"{system.path}/getGJLevels21.php", response_class=HTMLResponse)
@cache(
    ttl=f"{redis.ttl}s",
    key="get_levels:{str}/{diff}/{demonFilter}{type}/{len}/{featured}/{epic}/{gauntlet}/{page}",
)
async def get_level(
        request: Request,
        str: str = Form(default=None),
        page: int = Form(default=None),
        type: int = Form(default=None),
        len: int | str = Form(default=None),
        accountID: int = Form(default=None),
        diff: int | str = Form(default=None),
        demonFilter: int = Form(default=None),
        featured: int = Form(default=None),
        epic: int = Form(default=None),
        coins: int = Form(default=None),
        song: int = Form(default=None),
        gauntlet: int = Form(default=None),
        customSong: int = Form(default=None),
        db: AsyncSession = Depends(get_db),
):
    if str is not None:
        if "," in str:
            print('clen')
            result = await LevelService.get_levels_group(db=db, levels=str.split(","))
            is_gauntlet = False
            page = 0
            return await LevelGroup(service=result).GDGet_level(
                page=page, is_gauntlet=is_gauntlet
            )
    if diff not in ['-', None]:
        difficulty = Difficulty(int(diff))
    else:
        difficulty = None
    if epic == 1 or featured == 1:
        if epic == 1 and featured == 1:
            rate = (int(epic), int(featured))
        else:
            if epic == 1 and featured != 1:
                rate = 2
            if epic != 1 and featured == 1:
                rate = 1
    else:
        rate = 0
    scheme = GetLevel(
        lenght=len if len != "-" else None,
        string=str,
        searchType=type,
        accountID=accountID,
        difficulty=difficulty,
        demonFilter=demonFilter,
        page=page,
        rate=rate,
        coins=coins,
        song=song,
        customSong=customSong,
        gauntlet=gauntlet,
    )
    if gauntlet != None:
        result = await LevelService.get_gauntlets_levels(db=db, indexpack=gauntlet)
        page = 0
        is_gauntlet = True
    else:
        result = await LevelService().test_get_levels(db=db, data=scheme)
        print(result)
        page = page
        is_gauntlet = False
    if result["status"] == "ok":
        return await LevelGroup(service=result).GDGet_level(
            page=page, is_gauntlet=is_gauntlet
        )
    else:
        error(result["details"])
        return


@router.post(f"{system.path}/downloadGJLevel22.php", response_class=PlainTextResponse)
@cache(ttl=f"{redis.ttl}s", key="download_levels:{levelID}")
async def level_download(levelID: int = Form(), db: AsyncSession = Depends(get_db)):
    if int(levelID) < 0:  # daily & weekly
        service = await LevelService().get_level_buid(db=db, levelID=8)
        is_featured = True
    else:
        service = await LevelService().get_level_buid(db=db, levelID=levelID)
        is_featured = False
    match service['status']:
        case 'ok':
            object_level = await LevelObject(service=service, db=db).GDDownload_level(
                is_featured=is_featured
            )
            return object_level
        case 'error':
            error(service['details'])


@router.post(f"{system.path}/deleteGJLevelUser20.php", response_class=PlainTextResponse)
async def level_delete(
        accountID: int = Form(),
        gjp: str = Form(),
        levelID: int = Form(),
        db: AsyncSession = Depends(get_db),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        level_object = await LevelService().get_level_buid(db=db, levelID=levelID)
        if level_object['database'].authorID == int(accountID):
            await LevelService().delete_level(db=db, levelID=levelID)
            return "1"


def return_hash(string):
    hash_object = hashlib.sha1(bytes(string + "xI25fpAapCQg", "utf-8"))
    return hash_object.hexdigest()


@router.post(f"{system.path}/getGJGauntlets21.php", response_class=PlainTextResponse)
async def gauntlets(db: AsyncSession = Depends(get_db)):
    gauntlets = (await db.execute(select(models.Gauntlets))).scalars().all()
    await LevelService.get_gauntlets_levels(db=db, indexpack=2)
    response = ""
    hash_string = ""
    for gn in gauntlets:
        single_response = {1: gn.indexpack, 3: gn.levels}

        hash_string += f"{gn.indexpack}{gn.levels}"
        response += gd_dict_str(single_response) + "|"

    response = response[:-1] + f"#{return_hash(hash_string)}"
    return response


@router.post(f"{system.path}/getGJMapPacks21.php", response_class=PlainTextResponse)
async def map_packs(page: str = Form(), db: AsyncSession = Depends(get_db)):
    packs = await LevelService.get_map_packs(db=db, page=int(page))
    packstrings = []
    packhash = ""
    for pack in packs["database"]:
        packstrings.append(
            gd_dict_str(
                {
                    1: pack.id,
                    2: pack.name,
                    3: pack.levels,
                    4: pack.stars,
                    5: pack.coins,
                    6: pack.difficulty,
                    7: pack.text_color,
                    8: pack.bar_color,
                }
            )
        )
        packhash += f"{str(pack.id)[0]}{str(pack.id)[-1]}{pack.stars}{pack.coins}"
    return (
            "|".join(packstrings)
            + f"#{packs['count']}:{int(page) * 10}:10#"
            + return_hash(packhash)
    )


@router.post(f"{system.path}/getGJDailyLevel.php", response_class=PlainTextResponse)
async def get_daily_level():
    return "712111|4"
