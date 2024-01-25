from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import PlainTextResponse

from src.depends.context import Context
from src.objects.schemas import UpdateStats
from src.objects.userObject import UserObject, UserGroup
from src.schemas.users.errors import UserNotFoundError
from src.services.user import UserService
from src.utils.security import checkValidGJP2
from fastapi import Request
router = APIRouter(prefix="", tags=["Profile"])


@router.post("/getGJUserInfo20.php", response_class=PlainTextResponse)
async def get_userInfo(
    context: Context,
    targetAccountID: int = Form(),

):
    async with context:
        try:
            user = await context.services.users.get_user_byid(targetAccountID)

            return PlainTextResponse(await user.GDGetUser())

        except UserNotFoundError:
            return PlainTextResponse("-1")


@router.post(
    "/getGJAccountComments20.php", response_class=PlainTextResponse
)
async def get_posts(
    context: Context,
    accountID: int = Form(),
    page: int = Form(),
):
    async with context:
        try:
            user = (
                await context.services.users.get_user_byid(id=accountID)
            )
            return await user.GDGetUserPosts(ctx=context,page=page)
        except UserNotFoundError:
            return PlainTextResponse("-1")

@router.post("/getGJUsers20.php", response_class=PlainTextResponse)
async def get_user(str: str = Form()):
    service = await UserService.get_users_byName(name=str, db=db)
    usr = await UserGroup(service).GDGetUserGroup()
    return usr


@router.post("/updateGJUserScore22.php", response_class=PlainTextResponse)
async def updateGJUserScore22(
    context: Context,
    accountID: int = Form(),
    stars: int = Form(),
    demons: int = Form(),
    diamonds: int = Form(),
    moons: int = Form(),
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
    accJetpack: int = Form(),
    accSwing: int = Form(),
    accExplosion: int = Form(),
    gjp2: str = Form(),
    color1: int = Form(),
    color2: int = Form(),
    color3: int = Form()
):
    async with context:
        if await checkValidGJP2(ctx=context, id=accountID, gjp2=gjp2):
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
            await context.services.users.update_user(data=result)
            return str(accountID)
        else:
            raise HTTPException(401, "bro you dump")


#     db(f"UPDATE `users` SET  `iconkit` = '{iconkit}',`stars`='{stars}',`diamonds`='{diamonds}',`coins`='{coins}',`usr_coins`='{userCoins}',`demons`='{demons}' WHERE `id` = {accountID} ")
