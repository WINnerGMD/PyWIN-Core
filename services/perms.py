from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sql import models
from config import default_role
from objects.schemas import RateLevel

"yep i from Perm"

class PermissionService:
    

    @staticmethod
    async def get_permissions(id, db: AsyncSession):
        if id != None or 0:
            return (await db.execute(select(models.Roles).filter(models.Roles.id == id))).scalars().first()
        else:
            return (await db.execute(select(models.Roles).filter(models.Roles.id == default_role))).scalars().first()
    
    @classmethod
    async def request_access(cls, id, db: AsyncSession):
        user_obj = (await db.execute(select(models.Users).filter(models.Users.id == id))).scalars().first()
        return (await cls.get_permissions(id=user_obj.role, db=db)).typeMod

    


# class RateService:


#     def RateLevel(self, db:Session, data: RateLevel):
        