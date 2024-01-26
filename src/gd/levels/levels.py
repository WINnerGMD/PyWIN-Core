import datetime

from fastapi import APIRouter, Form, Request
from fastapi.responses import PlainTextResponse
from fastapi_events.dispatcher import dispatch

from events import Events
from ... helpers.rate import Difficulty
from ... objects.levelObject import LevelGroup, LevelObject
from ... depends.context import Context
from ... objects.schemas import UploadLevel
from ... schemas.levels.service.get import GetLevel
from ... services.daily import DailyService
from ... services.levels import LevelService
from ... utils.security import checkValidGJP2
from ... schemas.levels.errors import *
router = APIRouter(tags=["Levels"])


@router.post("/uploadGJLevel21.php")
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
        # dispatch(Events.NewLevel, LevelObject(service))
        if service["status"] == "ok":
            print("its okey")
            return service["level"].id
        else:
            error(service["details"])
            return "-1"
    else:
        print("ups")
        return "-1"


@router.post("/getGJLevels21.php")
# @cache(
#     ttl=f"{redis.ttl}s",
#     key="get_levels:{str}/{diff}/{demonFilter}{type}/{len}/{featured}/{epic}/{gauntlet}/{page}",
# )
async def get_level(
        context: Context,
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
    async with context:
        if str is not None:
            if "," in str:
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
                result = await context.services.levels.test_get_levels(scheme)
            except LevelNotFoundError:
                return PlainTextResponse("-1", 200)

        page = page
        is_gauntlet = False
        return await LevelGroup(service=result).GDGet_level(
                page=page, is_gauntlet=is_gauntlet
            )



@router.post("/downloadGJLevel22.php")
# @cache(ttl=f"{redis.ttl}s", key="download_levels:{levelID}")
async def level_download(
        ctx: Context,
        levelID: int = Form()):
    async with ctx:
        if int(levelID) < 0:  # daily & weekly
            level = await ctx.database.levels.find_byid(32)
            is_featured = True
        else:
            level = await ctx.services.levels.get_level_buid(levelID)
            is_featured = False

        object_level = await level.GDDownload_level(
            is_featured=is_featured
                )
        return object_level



@router.post("}/deleteGJLevelUser20.php")
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










@router.post("/getGJDailyLevel.php")
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
