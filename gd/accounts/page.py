from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import PlainTextResponse, HTMLResponse
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from services.user import UserService
from services.perms import PermissionService
from sql import models
import json
from config import system
from objects.schemas import UpdateStats
from objects.levelObject import LevelObject
from services.levels import LevelService
from utils.crypt import checkValidGJP
from config import system
from objects.userObject import UserObject
from logger import info, error

router = APIRouter(prefix="", tags=["Accounts"])


@router.post(f"{system.path}/getGJUserInfo20.php", response_class=PlainTextResponse)
async def get_userInfo(
    accountID: str = Form(default=0),
    targetAccountID: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    service = await UserService().get_user_byid(db=db, id=targetAccountID)
    if service["status"] == "ok":
        usr_obj = await UserObject(service=service, db=db).GDGetUser()
        info(f"get user {service['database'].userName}")
        return usr_obj
    else:
        error(f"failed to load user /// {service['details']})")


@router.post(f"{system.path}/getGJAccountComments20.php", response_class=PlainTextResponse)
async def get_posts(
    accountID: str = Form(),
    page: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    service = await UserService().get_user_byid(db=db, id=accountID)
    return await UserObject(service=service, db=db).GDGetUserPosts(page=page)


@router.post(f"{system.path}/updateGJUserScore22.php", response_class=PlainTextResponse)
async def updateGJUserScore22(
    accountID: str = Form(default=None),
    stars: str = Form(),
    demons: str = Form(),
    diamonds: str = Form(),
    coins: str = Form(),
    userCoins: str = Form(),
    accIcon: str = Form(),
    accShip: str = Form(),
    accBall: str = Form(),
    accBird: str = Form(),
    accDart: str = Form(),
    accRobot: str = Form(),
    accGlow: str = Form(),
    accSpider: str = Form(),
    accExplosion: str = Form(),
    gjp: str = Form(default=None),
    color1: str = Form(),
    color2: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    if accountID != None:
        if await checkValidGJP(id=accountID, gjp=gjp, db=db):
            iconkit = {
                "color1": int(color1),
                "color2": int(color2),
                "accBall": int(accBall),
                "accBird": int(accBird),
                "accDart": int(accDart),
                "accGlow": int(accGlow),
                "accIcon": int(accIcon),
                "accShip": int(accShip),
                "accRobot": int(accRobot),
                "accSpider": int(accSpider),
                "accExplosion": int(accExplosion),
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
            return accountID
        else:
            raise HTTPException(401, "bro you dump")


#     db(f"UPDATE `users` SET  `iconkit` = '{iconkit}',`stars`='{stars}',`diamonds`='{diamonds}',`coins`='{coins}',`usr_coins`='{userCoins}',`demons`='{demons}' WHERE `id` = {accountID} ")
