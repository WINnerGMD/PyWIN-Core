from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from src.depends.context import Context
from config import system
from src.objects.levelObject import LevelObject
from src.services.levels import LevelService

router = APIRouter()


@router.post(
    f"/likeGJItem211.php", response_class=PlainTextResponse, tags=["Misc"]
)
async def like_item(
    context: Context,
    itemID: str = Form(),
    liketype: int = Form(alias="type"),
    accountID: str = Form(),
    like: int = Form(),
):
    async with context:
        if liketype == 1:
            if like == 1:
                like = await (await LevelService(context).get_level_buid(itemID)).like(accountID)

                if like["status"] == "ok":
                    context.console.info("Like")
                    return "1"

            elif like == 0:
                dislike = await (await LevelService(context).get_level_buid(itemID)).dislike(accountID)

                if dislike["status"] == "ok":
                    context.console.info("Dislike")
                    return "1"


# class testClass:
#    __slots__ =
