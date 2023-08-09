from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sql import models

class LeaderBoardsService:
    
    @staticmethod
    async def leaderboard( db: AsyncSession):
        data = select(models.Users).order_by(models.Users.stars.desc())
        # return db.query(models.Users).order_by(models.Users.stars.desc()).all()
        return (await db.execute(data)).scalars().all()