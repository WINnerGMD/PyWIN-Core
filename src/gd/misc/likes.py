from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse

from ... config import system
from ... objects.levelObject import LevelObject
from ... services.levels import LevelService

router = APIRouter()


@router.post(
    f"{system.path}/likeGJItem211.php", response_class=PlainTextResponse, tags=["Misc"]
)
async def like_item(
    itemID: str = Form(),
    liketype: int = Form(alias="type"),
    accountID: str = Form(),
    like: int = Form(),
):
    if liketype == 1:
        if like == 1:
            service = await LevelService.get_level_buid(levelID=itemID)

            like = await LevelObject(service=service).like(accountID=accountID)
            if like["status"] == "ok":
                info("Like")
                return "1"

        elif like == 0:
            service = await LevelService.get_level_buid(levelID=itemID)

            like = await LevelObject(service=service).dislike(
                accountID=accountID
            )
            if like["status"] == "ok":
                info("Dislike")
                return "1"


# class testClass:
#    __slots__ =
