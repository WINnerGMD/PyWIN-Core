from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sql import models
from config import default_role
from objects.schemas import RateLevel
class PermissionService:
    


    async def get_permissions(self, id, db: AsyncSession):
        if id != None or 0:
            return (await db.execute(select(models.Roles).filter(models.Roles.id == id))).scalars().first()
        else:
            return (await db.execute(select(models.Roles).filter(models.Roles.id == default_role))).scalars().first()
    

    def request_access(self, id, db: AsyncSession):
        user_obj = db.query(models.Users).filter(models.Users.id == id).first()
        return self.get_permissions(id=user_obj.role, db=db).typeMod

    


# class RateService:


#     def RateLevel(self, db:Session, data: RateLevel):
        