from fastapi import APIRouter
router = APIRouter(prefix="/scores", tags=["Scores"])


# @router.get("/")
# async def get_scores() -> Leaderboard:
#     return await LeaderBoardsService.leaderboard("top")