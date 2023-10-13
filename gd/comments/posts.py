from datetime import datetime

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from database import get_db
from objects.schemas import UploadPost
from services.comments import PostCommentsService
from utils.crypt import checkValidGJP
from utils.gdform import formatted_date

router = APIRouter(tags=['Posts'])


@router.post(f"{system.path}/uploadGJAccComment20.php",
)
async def Upload_post(
    db: AsyncSession = Depends(get_db),
    accountID: int = Form(),
    comment: str = Form(),
    gjp: str = Form(),
):
    timestamp = formatted_date()
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        post_object = UploadPost(
            accountID=accountID, content=comment, timestamp=timestamp
        )
        await PostCommentsService().upload_post(db=db, data=post_object)
        return "1"
    else:
        raise HTTPException(401, "удачи!!!")


@router.post(f"{system.path}/deleteGJAccComment20.php", response_class=PlainTextResponse)
async def get_posts(
    accountID: int = Form(),
    gjp: str = Form(),
    commentID: int = Form(),
    db: AsyncSession = Depends(get_db),
):
    if await checkValidGJP(id=accountID, gjp=gjp, db=db):
        await PostCommentsService.delete_post(postID=commentID, db=db)

    return "1"
