from sqlalchemy import Update, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from logger import error
from src.objects.schemas import UpdateStats
from src.services.perms import PermissionService
from src.models import UsersModel, MessagesModel
from src.utils.crypt import bcrypt_hash


class UserService:
    @staticmethod
    async def register_user(
        db: AsyncSession, userName: str, password: str, mail: str, ip: str
    ):
        request = select(UsersModel).filter(UsersModel.userName == userName)
        if (await db.execute(request)).scalars().first() is not None:
            return {"code": "-2", "message": "error [UserName already registered]"}
        elif (
            await db.execute(select(UsersModel).filter(UsersModel.mail == mail))
        ).scalars().first() is not None:
            return {"code": "-3", "message": "error [User email already registered]"}
        else:
            passhash = bcrypt_hash(password)
            if system.auto_verified:
                db_user = UsersModel(
                    userName=userName,
                    passhash=passhash,
                    mail=mail,
                    ip=ip,
                    verified=True,
                )
            else:
                db_user = UsersModel(
                    userName=userName, passhash=passhash, mail=mail, ip=ip
                )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            return {"code": "1", "message": "success"}

    @staticmethod
    async def get_user_byid(db: AsyncSession, id: int):
        try:
            user = (
                (await db.execute(select(UsersModel).filter(UsersModel.id == id)))
                .scalars()
                .first()
            )
            if user is None:
                raise Exception("User not found")

            rank = len(
                (
                    await db.execute(
                        select(UsersModel).filter(UsersModel.stars >= user.stars)
                    )
                )
                .scalars()
                .all()
            )
            permissions = await PermissionService.get_permissions(id=user.role, db=db)
            print(user.role)
            print(permissions)
            return {
                "status": "ok",
                "database": user,
                "rank": rank,
                "permissions": permissions,
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
    async def update_user(db: AsyncSession, data: UpdateStats):
        smtp = (
            Update(UsersModel)
            .where(data.id == UsersModel.id)
            .values(data.dict(exclude_unset=True))
        )
        result = await db.execute(smtp)
        await db.commit()

        return result

    @staticmethod
    async def login_user(userName: str, password: str, db=AsyncSession):
        user = (
            (
                await db.execute(
                    select(UsersModel).filter(UsersModel.userName == userName)
                )
            )
            .scalars()
            .first()
        )
        passhash = bcrypt_hash(password)
        if user is None:
            return {"status": "error", "code": "-11", "message": "error [User not found]"}
        else:
            if user.passhash == passhash:
                if user.verified:
                    return {"status": "success", "code": "1", "message": f"{user.userName} successfully logged in", "id": user.id}
                else:
                    return {
                        "status": "error",
                        "code": "-12",
                        "message": "error [the user's account is disabled]",
                    }
            else:
                return {
                    "status": "error",
                    "code": "-11",
                    "message": "error [user's login credentials are incorrect]",
                }

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
