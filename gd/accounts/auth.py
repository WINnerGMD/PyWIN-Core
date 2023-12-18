from config import system
from fastapi.responses import PlainTextResponse
from fastapi import Request, Form, Depends, APIRouter

from services.user import UserService
from logger import error, info
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


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
    db: AsyncSession = Depends(get_db),
):
    service_response = await UserService().register_user(
        db=db, userName=userName, password=password, mail=email, ip=request.client.host
    )
    return str(service_response["code"])


@router.post(f"{system.path}/accounts/loginGJAccount.php")
async def login(
    userName: str = Form(), password: str = Form(), db: AsyncSession = Depends(get_db)
):
    service_response = await UserService().login_user(
        userName=userName, password=password, db=db
    )

    if service_response["status"] == "error":
        error(service_response)
        return str(service_response["code"])
    else:
        info(service_response['message'])
        return f"{service_response['id']},{service_response['id']}"
