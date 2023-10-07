from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from helpers.scores import  LeaderBoards
from sql import models
from config import system


class LeaderBoardsService:
    @staticmethod
    async def leaderboard(db: AsyncSession, scores_type: LeaderBoards ):
        match scores_type:
            case LeaderBoards.StarsList:
                data = select(models.Users).limit(system.leaderboards_limit).order_by(models.Users.stars.desc())
                result = (await db.execute(data)).scalars().all()
                return {'database':  result, 'count': len(result)}
            case LeaderBoards.CreatorList:
                data = select(models.Users).filter(models.Users.cp > 0).limit(system.leaderboards_limit).order_by(models.Users.cp.desc())
                result= (await db.execute(data)).scalars().all()
                return {'database': result, 'count': len(result)}
