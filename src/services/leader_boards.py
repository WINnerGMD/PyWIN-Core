from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.helpers.scores import LeaderBoards
from src.models import UsersModel
from config import system
from src.depends.context import Context
from src.schemas.scores.get import Place, Leaderboard

class LeaderBoardsService:
    @staticmethod
    async def leaderboard(scores_type: LeaderBoards, ctx: Context) -> Leaderboard:
        match scores_type:
            case LeaderBoards.StarsList:
                data = (
                    select(UsersModel)
                    .limit(system.leaderboards_limit)
                    .order_by(UsersModel.stars.desc())
                )
            case LeaderBoards.CreatorList:
                data = (
                    select(UsersModel)
                    .filter(UsersModel.cp > 0)
                    .limit(system.leaderboards_limit)
                    .order_by(UsersModel.cp.desc())
                )
            case LeaderBoards.GlobalList:
                raise NotImplementedError
            case LeaderBoards.FriendsList:
                raise NotImplementedError
        result = [Place(place=c, user=i) for c, i in enumerate((await UsersRepository.find_bySTMT(data)).all())]
        return Leaderboard(count=len(result), leaders=result)
