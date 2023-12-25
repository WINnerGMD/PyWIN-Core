from config import system
from fastapi.responses import PlainTextResponse
from fastapi import Request, Form, Depends, APIRouter

from src.services.user import UserService, UsersModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.crypt import checkValidGJP2byName
from src.schemas.auth.errors import *
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="", tags=["Auth"])


@router.post(
    f"{system.path}/accounts/registerGJAccount.php",
    response_class=PlainTextResponse,
)
async def register_account(
        request: Request,
        userName: str = Form(),
        password: str = Form(),
        email: str = Form(),
) -> PlainTextResponse:
    """
     Register endpoint

     Return status code
    """
    try:
        await UserService().register_user(
            userName=userName, password=password, mail=email, ip=request.client.host
        )
        return PlainTextResponse("1", 200)

    # errors validate
    except UsernameIsAlreadyInUseError:
        return PlainTextResponse("-2", 200)

    except EmailIsAlreadyInUseError:
        return PlainTextResponse("-3", 200)


@router.post(f"{system.path}/accounts/loginGJAccount.php")
async def login(
        userName: str = Form(),
        gjp2: str = Form()
) -> PlainTextResponse:
    """
     Login endpoint
     Return userid or error code
    """
    try:
        user: UsersModel = await UserService.login_user(userName, gjp2)
        return f"{user.id},{user.id}"

    # validate errors
    except InvalidCreditionalsError:
        return PlainTextResponse("-11", 200)

    except AccountIsDisabledError:
        return PlainTextResponse("-12", 200)
