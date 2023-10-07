from fastapi import APIRouter, Form, Depends
from config import system
from fastapi.responses import PlainTextResponse
from services.comments import CommentsService
from objects.schemas import UploadComments
from sqlalchemy.orm import Session
from database import get_db
from services.user import UserService
from datetime import datetime
from utils.gdform import gd_dict_str
from utils.crypt import checkValidGJP
router = APIRouter(tags=['Comments'])


@router.post(f"{system.path}/uploadGJComment21.php", response_class=PlainTextResponse)
async def upload_comment(
    accountID: str = Form(default=None),
    userName: str = Form(default=None),
    comment: str = Form(default=None),
    levelID: str = Form(default=None),
    percent: str = Form(default=None),
    gjp: str = Form(),
    db: Session = Depends(get_db),
):
    if await checkValidGJP(accountID, gjp, db):
        comment_object = UploadComments(
            userName=userName,
            accountID=accountID,
            comment=comment,
            levelID=levelID,
            percent=percent,
        )
        answer = await CommentsService().upload_comments(db=db, data=comment_object)
        if answer["status"] == "ok":
            if answer["type"] == "comment":
                return str(answer["data"].id)

@router.post(f"{system.path}/getGJComments21.php", response_class=PlainTextResponse)
async def get_user(
    db: Session = Depends(get_db), levelID: str = Form(), page: str = Form()
):
    comments_object = await CommentsService().get_comments(db=db, level_id=levelID,page=page)
    if comments_object["status"] == "ok":
        comment_string = []
        for i in comments_object['database']:
            userObject = (await UserService().get_user_byid(db=db, id=i.authorId))['database']
            iconkits = userObject.iconkits

            comment_string.append(
                (
                gd_dict_str(
                    {
                        2: i.content,
                        3: i.authorId,
                        4: i.likes,
                        6: i.id,
                        7: i.is_spam,
                        8: i.id,
                        9: "aof",
                        10: i.progress,
                    },
                    separator="~"
                )
            ) + ":" + gd_dict_str(
                    {
                        1: i.authorName,
                        9: iconkits['accIcon'],
                        10: iconkits['color1'],
                        11: iconkits['color2'],
                        14: 0,
                        15: 0,
                        16: i.authorId
                    },
                    separator="~"
                )


            )
        return "|".join(comment_string) + f"#{comments_object['count']}:{system.page * page}:{system.page}"
