from fastapi import APIRouter, Depends
from src.services.user import UserService
from logger import info

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{usrid}")
async def get_user(usrid):
    info(f"Request to api | /api/users/{usrid}")
    userData = (await UserService.get_user_byid(id=usrid))["database"]
    return {
        "status": "ok",
        "userName": userData.userName,
        "role": userData.role,
        "stats": {
            "stars": userData.stars,
            "diamonds": userData.diamonds,
            "coins": userData.coins,
            "iconkits": userData.iconkits,
        },
    }
