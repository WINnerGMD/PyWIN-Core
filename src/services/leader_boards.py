from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.helpers.scores import LeaderBoards
from models import UsersModel
from config import system


class LeaderBoardsService:
    @staticmethod
    async def leaderboard(db: AsyncSession, scores_type: LeaderBoards):
        match scores_type:
            case LeaderBoards.StarsList:
                data = (
                    select(UsersModel)
                    .limit(system.leaderboards_limit)
                    .order_by(UsersModel.stars.desc())
                )
                result = (await db.execute(data)).scalars().all()
                return {"database": result, "count": len(result)}
            case LeaderBoards.CreatorList:
                data = (
                    select(UsersModel)
                    .filter(UsersModel.cp > 0)
                    .limit(system.leaderboards_limit)
                    .order_by(UsersModel.cp.desc())
                )
                result = (await db.execute(data)).scalars().all()
                return {"database": result, "count": len(result)}
