from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from logger import info, error
from src.objects.schemas import UpdateStats
from src.objects.userObject import UserObject, UserGroup
from src.services.user import UserService
from src.utils.crypt import checkValidGJP2

router = APIRouter(prefix="", tags=["Profile"])


@router.post(f"{system.path}/getGJUserInfo20.php", response_class=PlainTextResponse)
async def get_userInfo(
    targetAccountID: int = Form(),
):
    service = await UserService().get_user_byid(db=db, id=targetAccountID)
    if service["status"] == "ok":
        usr_obj = await UserObject(service=service, db=db).GDGetUser()
        info(f"get user {service['database'].userName}")
        return usr_obj
    else:
        error(f"failed to load user /// {service['details']})")


@router.post(
    f"{system.path}/getGJAccountComments20.php", response_class=PlainTextResponse
)
async def get_posts(
    accountID: int = Form(),
    page: int = Form(),
):
    service = await UserService().get_user_byid(db=db, id=accountID)
    return await UserObject(service=service, db=db).GDGetUserPosts(page=page)


@router.post(f"{system.path}/getGJUsers20.php", response_class=PlainTextResponse)
async def get_user(str: str = Form()):
    service = await UserService.get_users_byName(name=str, db=db)
    usr = await UserGroup(service).GDGetUserGroup()
    return usr


@router.post(f"{system.path}/updateGJUserScore22.php", response_class=PlainTextResponse)
async def updateGJUserScore22(
    accountID: int = Form(),
    stars: int = Form(),
    demons: int = Form(),
    diamonds: int = Form(),
    coins: int = Form(),
    userCoins: int = Form(),
    accIcon: int = Form(),
    accShip: int = Form(),
    accBall: int = Form(),
    accBird: int = Form(),
    accDart: int = Form(),
    accRobot: int = Form(),
    accGlow: int = Form(),
    accSpider: int = Form(),
    accExplosion: int = Form(),
    gjp: str = Form(),
    color1: int = Form(),
    color2: int = Form(),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        iconkit = {
            "color1": color1,
            "color2": color2,
            "accBall": accBall,
            "accBird": accBird,
            "accDart": accDart,
            "accGlow": accGlow,
            "accIcon": accIcon,
            "accShip": accShip,
            "accRobot": accRobot,
            "accSpider": accSpider,
            "accExplosion": accExplosion,
        }
        result = UpdateStats(
            id=accountID,
            stars=stars,
            demons=demons,
            diamonds=diamonds,
            coins=coins,
            usr_coins=userCoins,
            iconkits=iconkit,
        )
        await UserService().update_user(db=db, data=result)
        return str(accountID)
    else:
        raise HTTPException(401, "bro you dump")


#     db(f"UPDATE `users` SET  `iconkit` = '{iconkit}',`stars`='{stars}',`diamonds`='{diamonds}',`coins`='{coins}',`usr_coins`='{userCoins}',`demons`='{demons}' WHERE `id` = {accountID} ")
