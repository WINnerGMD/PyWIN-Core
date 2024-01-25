from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from src.objects.schemas import UpdateStats
from src.models import UsersModel, MessagesModel
from typing import TYPE_CHECKING
from src.schemas.users.errors import *
from src.schemas.errors import SQLAlchemyNotFound
from src.objects.userObject import UserObject
from typing import Any

if TYPE_CHECKING:
    import src.abstract.context as abc


class UserService:

    def __init__(self, ctx: 'abc.AbstractContext'):
        self.ctx = ctx

    @staticmethod
    async def register_user(
            userName: str, password: str, mail: str, ip: str,
    ) -> None:
        async with ctx:
            request = UsersModel.userName == userName
            request2 = UsersModel.mail == mail
            if (await ctx.database.users.find_byfield(request)).first() is not None:
                raise UsernameIsAlreadyInUseError

            elif (await ctx.database.users.find_byfield(request2)).first() is not None:
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
                ctx.console.alert("SUKA")
                await ctx.database.users.add_one(db_user)
                await ctx.commit()

    async def get_user_byid(self, id: int) -> UserObject:
        async with self.ctx:
            try:
                user = UserObject(await self.ctx.database.users.find_byid(id))

                return user

            except SQLAlchemyNotFound:
                raise UserNotFoundError

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

    async def update_user(self, data: UpdateStats):
        result = await self.ctx.database.users.update(data.id, data.dict(exclude_unset=True))
        return result

    @staticmethod
    async def login_user(ctx: 'abc.AbstractContext', userName: str, password: str) -> Any:
        """
        Logic of user login
        """
        user = (await ctx.database.users.find_byfield(UsersModel.userName == userName)).first()
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
