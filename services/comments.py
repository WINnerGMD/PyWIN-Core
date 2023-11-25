from types import FunctionType

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from config import system
from helpers.commands import Commands
from helpers.rate import Difficulty
from models import CommentsModel, LevelsModel, PostsModel
from objects.schemas import UploadComments, UploadPost
from services.user import UserService
from utils.crypt import base64_decode


def methods(cls):
    result = []
    for x, y in cls.__dict__.items():
        if type(y) == FunctionType and x.startswith("__") != True:
            result.append({"name": x, "func": y})
    return result


command_list = methods(Commands)


class CommentsService:
    @staticmethod
    async def get_comments(level_id, page: int, db: AsyncSession):
        comments = (
            (
                await db.execute(
                    select(CommentsModel)
                    .filter(CommentsModel.levelID == level_id)
                    .order_by(CommentsModel.id.desc())
                    .limit(system.page)
                    .offset(system.page * page)
                )
            )
            .scalars()
            .all()
        )
        count = len(
            (
                await db.execute(
                    select(CommentsModel).filter(CommentsModel.levelID == level_id)
                )
            )
            .scalars()
            .all()
        )
        if comments is not None:
            return {"status": "ok", "database": comments, "count": count}
        else:
            return {"status": "error", "details": "comments not found"}

    @classmethod
    async def upload_comments(cls, db: AsyncSession, data: UploadComments) -> dict:
        try:
            content = base64_decode(data.comment)
            print(content)
            if content.startswith("/"):
                await cls.commands_handler(
                    data=content[1:],
                    levelID=data.levelID,
                    authorID=data.accountID,
                    db=db,
                )
                return {"status": "ok", "type": "command"}
            else:
                db_comment = CommentsModel(
                    authorId=data.accountID,
                    content=data.comment,
                    progress=data.percent,
                    levelID=data.levelID,
                    authorName=(
                        (await UserService().get_user_byid(db=db, id=data.accountID))
                    )["database"].userName,
                )
                db.add(db_comment)
                await db.commit()
                await db.refresh(db_comment)

                return {"status": "ok", "type": "comment", "data": db_comment}
        except Exception as e:
            return {"status": "error", "details": e}

    @staticmethod
    async def commands_handler(
        data: str, levelID: int, authorID: int, db: AsyncSession
    ) -> bool:
        data = data.split(" ")
        name = data[0]
        commands = data[1:]
        print(name)
        match name:
            case "rate":
                if (await UserService.get_user_byid(id=authorID, db=db))[
                    "permissions"
                ].rateLevels:
                    print(commands)
                    match commands[0]:
                        case "easy":
                            difficulty = Difficulty.easy
                        case "normal":
                            difficulty = Difficulty.normal
                        case "hard":
                            difficulty = Difficulty.hard
                        case "harder":
                            difficulty = Difficulty.harder
                        case "insane":
                            difficulty = Difficulty.insane
                        case "easydemon":
                            difficulty = Difficulty.easyDemon
                        case "mediumdemon":
                            difficulty = Difficulty.mediumDemon
                        case "harddemon":
                            difficulty = Difficulty.hardDemon
                        case "insanedemon":
                            difficulty = Difficulty.insaneDemon
                        case "extremedemon":
                            difficulty = Difficulty.extremeDemon
                    print(difficulty.value)
                    (
                        await db.execute(
                            update(LevelsModel)
                            .filter(LevelsModel.id == levelID)
                            .values(
                                {"difficulty": difficulty.value, "stars": commands[1]}
                            )
                        )
                    )

                    await db.commit()
            case "epic":
                if (await UserService.get_user_byid(id=authorID, db=db))[
                    "permissions"
                ].rateLevels:
                    (
                        await db.execute(
                            update(LevelsModel)
                            .filter(LevelsModel.id == levelID)
                            .values({"rate": 2})
                        )
                    )
                    await db.commit()
            case "featured":
                if (await UserService.get_user_byid(id=authorID, db=db))[
                    "permissions"
                ].rateLevels:
                    (
                        await db.execute(
                            update(LevelsModel)
                            .filter(LevelsModel.id == levelID)
                            .values({"rate": 1})
                        )
                    )
                    await db.commit()
            case "nonrate":
                if (await UserService.get_user_byid(id=authorID, db=db))[
                    "permissions"
                ].rateLevels:
                    (
                        await db.execute(
                            update(LevelsModel)
                            .filter(LevelsModel.id == levelID)
                            .values({"rate": 0})
                        )
                    )
                    await db.commit()
            case "norate":
                if (await UserService.get_user_byid(id=authorID, db=db))[
                    "permissions"
                ].rateLevels:
                    (
                        await db.execute(
                            update(LevelsModel)
                            .filter(LevelsModel.id == levelID)
                            .values({"rate": 0, "difficulty": 0, "stars": 0})
                        )
                    )
                    await db.commit()


class PostCommentsService:
    @staticmethod
    async def upload_post(db: AsyncSession, data: UploadPost):
        db_post = PostsModel(
            accountID=data.accountID, content=data.content, timestamp=data.timestamp
        )

        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)
        return db_post

    @staticmethod
    async def delete_post(postID, db: AsyncSession):
        db_level = (
            (await db.execute(select(PostsModel).filter(PostsModel.id == postID)))
            .scalars()
            .first()
        )
        await db.delete(db_level)
        await db.commit()

    @staticmethod
    async def get_post(db: AsyncSession, usrid: int, page: int):
        offset = int(page) * 10
        count = len(
            (
                await db.execute(
                    select(PostsModel).filter(PostsModel.accountID == usrid)
                )
            )
            .scalars()
            .all()
        )
        return {
            "database": (
                await db.execute(
                    select(PostsModel)
                    .filter(PostsModel.accountID == usrid)
                    .limit(10)
                    .offset(offset)
                    .order_by(PostsModel.id.desc())
                )
            )
            .scalars()
            .all(),
            "count": count,
        }
