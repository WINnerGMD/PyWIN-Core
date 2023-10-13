from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sql import models
from config import system
from objects.schemas import RateLevel

"Parma"


class PermissionService:
    @staticmethod
    async def get_permissions(id, db: AsyncSession):
        if id != 0:
            return (
                (await db.execute(select(models.Roles).filter(models.Roles.id == id)))
                .scalars()
                .first()
            )
        else:
            return (
                (
                    await db.execute(
                        select(models.Roles).filter(models.Roles.id == system.default_role)
                    )
                )
                .scalars()
                .first()
            )

