from fastapi import APIRouter, Form, Depends
from fastapi.responses import PlainTextResponse
from config import system
from src.services.user import UserService
from src.services.levels import LevelService
from src.objects.levelObject import LevelObject
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.crypt import checkValidGJP2
from src.helpers.rate import Difficulty
from logger import error

router = APIRouter(tags=["rate"], prefix="")


@router.post(f"{system.path}/suggestGJStars20.php", response_class=PlainTextResponse)
async def suggestGJStars(
    accountID: int = Form(),
    gjp: str = Form(),
    feature: int = Form(),
    levelID: int = Form(),
    stars: int = Form(),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        user = await UserService.get_user_byid(db=db, id=accountID)
        if user["permissions"].rateLevels:
            level = await LevelService.get_level_buid(levelID=levelID, db=db)
            match stars:
                case 1:
                    difficulty = Difficulty.gd_auto
                case 2:
                    difficulty = Difficulty.easy
                case 3:
                    difficulty = Difficulty.normal
                case 4 | 5:
                    difficulty = Difficulty.hard
                case 6 | 7:
                    difficulty = Difficulty.harder
                case 8 | 9:
                    difficulty = Difficulty.insane
                case 10:
                    difficulty = Difficulty.easyDemon
            object_level = await LevelObject(level, db=db).rate(
                stars=stars, difficulty=difficulty, rate=1 if feature == 1 else 0
            )
            if object_level["status"] == "ok":
                return "1"
            else:
                error(object_level["details"])
                return "-1"


@router.post(f"{system.path}/rateGJStars211.php", response_class=PlainTextResponse)
async def rate_stars(
    gjp: str = Form(),
    stars: int = Form(),
    levelID: int = Form(),
    accountID: int = Form(),
):
    if await checkValidGJP(accountID, gjp, db):
        level = await LevelService.get_level_buid(levelID, db)
        if level["status"] == "ok":
            match stars:
                case 1:
                    difficulty = Difficulty.gd_auto
                case 2:
                    difficulty = Difficulty.easy
                case 3:
                    difficulty = Difficulty.normal
                case 4 | 5:
                    difficulty = Difficulty.hard
                case 6 | 7:
                    difficulty = Difficulty.harder
                case 8 | 9:
                    difficulty = Difficulty.insane
                case 10:
                    difficulty = Difficulty.easyDemon
            level_obj = await LevelObject(level, db).user_rate(
                difficulty, stars, accountID
            )
            if level_obj["status"] == "ok":
                return 1
