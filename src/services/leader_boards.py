from sqlalchemy import select
from .. helpers.scores import LeaderBoards
from .. models import UsersModel
from .. config import system
from .. depends.context import Context
from .. schemas.scores.get import Place, Leaderboard

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
