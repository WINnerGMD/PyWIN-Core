from sqlalchemy import Update, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from logger import error
from src.objects.schemas import UpdateStats
from src.services.perms import PermissionService
from src.models import UsersModel, MessagesModel
from src.utils.crypt import bcrypt_hash, sha1_hash
from src.depends.user import UsersRepository
from src.schemas.users.errors import *
from typing import Any
class UserService:
    @staticmethod
    async def register_user(
            userName: str, password: str, mail: str, ip: str
    ):
        request = select(UsersModel).filter(UsersModel.userName == userName)
        request2 = select(UsersModel).filter(UsersModel.mail == mail)
        if await UsersRepository().findfirst_bySTMT(request) is not None:
            raise UsernameIsAlreadyInUseError

        elif await UsersRepository().findfirst_bySTMT(request2) is not None:
            raise EmailIsAlreadyInUseError

        else:
            passhash = await sha1_hash(password, "mI29fmAnxgTs")
            if system.auto_verified:
                db_user = UsersModel(
                    userName=userName,
                    passhash=passhash,
                    mail=mail,
                    ip=ip,
                    verified=True
                )

            else:
                db_user = UsersModel(
                    userName=userName,
                    passhash=passhash,
                    mail=mail,
                    ip=ip,
                )
            await UsersRepository().add_one(db_user)

    @staticmethod
    async def get_user_byid(id: int):
        try:
            user = await UsersRepository().find_byid(id)
            if user is None:
                raise UserNotFoundError

            return {
                "status": "ok",
                "database": user,
            }

        except Exception as ex:
            return {"status": "error", "details": ex}

    @staticmethod
    async def upload_message(db: AsyncSession, authorID, recipientID, subject, body):
        try:
            message = MessagesModel(
                authorID=authorID, recipientID=recipientID, subject=subject, body=body
            )
            db.add(message)
            await db.commit()
            await db.refresh(message)
            return "1"
        except Exception as ex:
            error(ex)
            return "-1"

    @staticmethod
    async def update_user(data: UpdateStats):
        result = UsersRepository().update(data.id, data.dict(exclude_unset=True))
        return result

    @staticmethod
    async def login_user(userName: str, password: str) -> Any:
        """
        Logic of user login
        """
        user: UsersModel = await UsersRepository().find_byfield(UsersModel.userName == userName)
        if user is None:
            raise InvalidCreditionalsError  
        else:
            if user.passhash == password:
                if user.verified:
                    return user
                else:
                    raise AccountIsDisabledError
            else:
                raise InvalidCreditionalsError

    @staticmethod
    async def get_users_byName(name, db: AsyncSession):
        query = select(UsersModel).where(UsersModel.userName.like(f"%{name}%"))
        result = (await db.execute(query)).scalars().all()
        count = len(result)
        return {"database": result, "count": count}

    @staticmethod
    async def get_total_users(db: AsyncSession):
        try:
            query = select(UsersModel)
            total = len((await db.execute(query)).scalars().all())
            return {"status": "ok", "count": total}
        except Exception as e:
            return {"status": "error", "details": e}
