from fastapi import APIRouter, Depends
from src.depends.context import Context

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{usrid}")
async def get_user(
    usrid: int,
    context: Context,
):
    async with context:
        user = await context.services.users.get_user_byid(usrid)
        return user
    # info(f"Request to api | /api/users/{usrid}")
    # userData = (await UserService.get_user_byid(id=usrid))["database"]
    # return {
    #     "status": "ok",
    #     "userName": userData.userName,
    #     "role": userData.role,
    #     "stats": {
    #         "stars": userData.stars,
    #         "diamonds": userData.diamonds,
    #         "coins": userData.coins,
    #         "iconkits": userData.iconkits,
    #     },
    # }
