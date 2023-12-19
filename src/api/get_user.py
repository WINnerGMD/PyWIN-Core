from fastapi import APIRouter, Depends
from src.services.user import UserService
from logger import info

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/users/{usrid}")
async def get_user(usrid):
    info(f"Request to api | /api/users/{usrid}")
    userData = (await UserService.get_user_byid(id=usrid, db=db))["database"]
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
