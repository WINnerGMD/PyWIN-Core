import datetime

from fastapi import APIRouter, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from fastapi_events.dispatcher import dispatch

from cache import cache
from config import system, redis
from events import Events
from logger import error
from src.helpers.rate import Difficulty
from src.objects.levelObject import LevelGroup, LevelObject
from src.depends.level import LevelsRepository
from src.objects.schemas import UploadLevel
from src.schemas.levels.service.get import GetLevel
from src.services.daily import DailyService
from src.services.levels import LevelService
from src.utils.crypt import checkValidGJP2
from src.schemas.levels.errors import *
router = APIRouter(prefix="", tags=["Levels"])


@router.post(f"{system.path}/uploadGJLevel21.php")
async def upload_level(
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
        gjp2: str = Form(),
):

    if await checkValidGJP2(accountID, gjp2=gjp2):
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
        service = await LevelService().upload_level(data=SystemObj)
        dispatch(Events.NewLevel, LevelObject(service))
        if service["status"] == "ok":
            print("its okey")
            return service["level"].id
        else:
            error(service["details"])
            return "-1"
    else:
        print("ups")
        return "-1"


@router.post(f"{system.path}/getGJLevels21.php", response_class=HTMLResponse)
@cache(
    ttl=f"{redis.ttl}s",
    key="get_levels:{str}/{diff}/{demonFilter}{type}/{len}/{featured}/{epic}/{gauntlet}/{page}",
)
async def get_level(
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
        result = await LevelService.get_gauntlets_levels(indexpack=gauntlet)
        page = 0
        is_gauntlet = True
    else:
        try:
            result = await LevelService().test_get_levels(scheme)
        except LevelNotFoundError:
            return PlainTextResponse("-1", 200)

    page = page
    is_gauntlet = False
    return await LevelGroup(service=result).GDGet_level(
            page=page, is_gauntlet=is_gauntlet
        )



@router.post(f"{system.path}/downloadGJLevel22.php", response_class=PlainTextResponse)
@cache(ttl=f"{redis.ttl}s", key="download_levels:{levelID}")
async def level_download(levelID: int = Form()):
    if int(levelID) < 0:  # daily & weekly
        service = await LevelsRepository().find_byid(32)
        is_featured = True
    else:
        service = await LevelsRepository().find_byid(levelID)
        is_featured = False

    object_level = await LevelObject(service=service).GDDownload_level(
        is_featured=is_featured
            )
    return object_level



@router.post(f"{system.path}/deleteGJLevelUser20.php", response_class=PlainTextResponse)
async def level_delete(
        accountID: int = Form(),
        gjp: str = Form(),
        levelID: int = Form(),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        level_object = await LevelService().get_level_buid(db=db, levelID=levelID)
        if level_object["database"].authorID == int(accountID):
            await LevelService().delete_level(db=db, levelID=levelID)
            return "1"










@router.post(f"{system.path}/getGJDailyLevel.php", response_class=PlainTextResponse)
async def get_daily_level(
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
