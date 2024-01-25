from fastapi import APIRouter, Form

from config import system
from src.objects.schemas import UploadComments
from src.services.comments import CommentsService
from src.services.user import UserService
from src.utils.security import checkValidGJP2
from src.utils.gdform import gd_dict_str

router = APIRouter(tags=["Comments"])


@router.post("/uploadGJComment21.php")
async def upload_comment(
    accountID: int = Form(default=None),
    userName: str = Form(default=None),
    comment: str = Form(default=None),
    levelID: int = Form(default=None),
    percent: int = Form(default=None),
    gjp2: str = Form(),
):
    if percent == None:
        percent = 0
    if await checkValidGJP2(accountID, gjp2):
        comment_object = UploadComments(
            userName=userName,
            accountID=accountID,
            comment=comment,
            levelID=levelID,
            percent=percent,
        )
        answer = await CommentsService().upload_comments(data=comment_object)
        if answer["status"] == "ok":
            if answer["type"] == "comment":
                return str(answer["data"].id)


@router.post("/getGJComments21.php")
async def get_comments(
   levelID: int = Form(), page: int = Form()
):
    comments_object = await CommentsService().get_comments(
       level_id=levelID, page=page
    )
    if comments_object["status"] == "ok":
        comment_string = []
        for i in comments_object["database"]:
            userObject = (await UserService().get_user_byid(id=i.authorId))[
                "database"
            ]
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
                            10: i.progress,
                        },
                        separator="~",
                    )
                )
                + ":"
                + gd_dict_str(
                    {
                        1: i.authorName,
                        9: iconkits["accIcon"],
                        10: iconkits["color1"],
                        11: iconkits["color2"],
                        14: 0,
                        15: 0,
                        16: i.authorId,
                    },
                    separator="~",
                )
            )
        return (
            "|".join(comment_string)
            + f"#{comments_object['count']}:{system.page * page}:{system.page}"
        )
