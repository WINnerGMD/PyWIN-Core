from datetime import datetime

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from src.objects.schemas import UploadPost
from src.services.comments import PostCommentsService
from src.utils.crypt import checkValidGJP2
from src.utils.gdform import formatted_date

router = APIRouter(tags=["Posts"])


@router.post(
    f"{system.path}/uploadGJAccComment20.php",
)
async def Upload_post(
    accountID: int = Form(),
    comment: str = Form(),
    gjp2: str = Form(),
):
    timestamp = formatted_date()
    if await checkValidGJP2(id=accountID, gjp2=gjp2):
        post_object = UploadPost(
            accountID=accountID, content=comment, timestamp=timestamp
        )
        await PostCommentsService().upload_post(data=post_object)
        return "1"
    else:
        raise HTTPException(401, "удачи!!!")


@router.post(
    f"{system.path}/deleteGJAccComment20.php", response_class=PlainTextResponse
)
async def get_posts(
    accountID: int = Form(),
    gjp: str = Form(),
    commentID: int = Form(),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        await PostCommentsService.delete_post(postID=commentID, db=db)

    return "1"
