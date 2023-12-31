import datetime
import hashlib

from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi_events.dispatcher import dispatch
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache import cache
from config import system, redis
from database import get_db
from events import Events
from helpers.rate import Difficulty
from logger import error
from models import GauntletsModel
from objects.levelObject import LevelGroup, LevelObject
from objects.schemas import GetLevel, UploadLevel
from services.daily import DailyService
from services.levels import LevelService
from utils.crypt import checkValidGJP
from utils.gdform import gd_dict_str

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
        password: str = Form(),
        original: int = Form(),
        twoPlayer: int = Form(),
        songID: str = Form(),
        objects: int = Form(),
        coins: int = Form(),
        requestedStars: int = Form(),
        ldm: int = Form(),
        gameVersion: int = Form(),
        gjp: str = Form(),
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
        dispatch(Events.NewLevel, LevelObject(service, db))
        if service["status"] == "ok":
            return service["level"].id
        else:
            error(service["details"])
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
            print("clen")
            result = await LevelService.get_levels_group(db=db, levels=str.split(","))
            is_gauntlet = False
            page = 0
            return await LevelGroup(service=result).GDGet_level(
                page=page, is_gauntlet=is_gauntlet
            )
    if diff not in ["-", None]:
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
        service = await LevelService().get_level_buid(db=db, levelID=32)
        is_featured = True
    else:
        service = await LevelService().get_level_buid(db=db, levelID=levelID)
        is_featured = False
    match service["status"]:
        case "ok":
            object_level = await LevelObject(service=service, db=db).GDDownload_level(
                is_featured=is_featured
            )
            return object_level
        case "error":
            error(service["details"])


@router.post(f"{system.path}/deleteGJLevelUser20.php", response_class=PlainTextResponse)
async def level_delete(
        accountID: int = Form(),
        gjp: str = Form(),
        levelID: int = Form(),
        db: AsyncSession = Depends(get_db),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        level_object = await LevelService().get_level_buid(db=db, levelID=levelID)
        if level_object["database"].authorID == int(accountID):
            await LevelService().delete_level(db=db, levelID=levelID)
            return "1"










@router.post(f"{system.path}/getGJDailyLevel.php", response_class=PlainTextResponse)
async def get_daily_level(db: AsyncSession = Depends(get_db),
                          weekly: int = Form(default=0)
                          ):

    match weekly:
        case 0:
            count = await DailyService.getCountDailyLevels(db)
            additional_id = 0
            daily = await DailyService.getLastDaily(db)
            time_last = daily.onTime - datetime.datetime.now()
        case 1:
            count = await DailyService.getCountWeeklyLevels(db)
            additional_id = 100001
            weekly = await DailyService.getLastWeekly(db)
            print(weekly.id)
            time_last = weekly.onTime - datetime.datetime.now()
            print(time_last.seconds)

    data = f"{count+ additional_id}|{time_last.seconds}"
    print(data)
    return data
