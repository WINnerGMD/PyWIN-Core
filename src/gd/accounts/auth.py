from fastapi import Request, Form, APIRouter

from ... services.user import UserService, UsersModel
from ... depends.context import Context
from ... schemas.users.errors import *
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/accounts", tags=["Auth"])


@router.post(
    "/registerGJAccount.php",
    response_class=PlainTextResponse,
)
async def register_account(
        context: Context,
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
            userName=userName, password=password, mail=email, ip=request.client.host, ctx=context
        )
        return PlainTextResponse("1", 200)

    # Validate errors
    except UsernameIsAlreadyInUseError:
        return PlainTextResponse("-2", 200)

    except EmailIsAlreadyInUseError:
        return PlainTextResponse("-3", 200)


@router.post("/loginGJAccount.php")
async def login(
        context: Context,
        userName: str = Form(),
        gjp2: str = Form()
) -> PlainTextResponse:
    """
     Login endpoint
     Return userid or error code
    """
    try:
        user: UsersModel = await UserService.login_user(context, userName, gjp2)
        return f"{user.id},{user.id}"

    # Validate errors
    except InvalidCreditionalsError:
        return PlainTextResponse("-11", 200)

    except AccountIsDisabledError:
        return PlainTextResponse("-12", 200)
