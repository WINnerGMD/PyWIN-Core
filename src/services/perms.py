from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import RolesModel
from config import system

"Parma"


class PermissionService:
    @staticmethod
    async def get_permissions(id, db: AsyncSession):
        if id != 0:
            return (
                (await db.execute(select(RolesModel).filter(RolesModel.id == id)))
                .scalars()
                .first()
            )
        else:
            return (
                (
                    await db.execute(
                        select(RolesModel).filter(RolesModel.id == system.default_role)
                    )
                )
                .scalars()
                .first()
            )
