import datetime
from types import FunctionType

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .. config import (system)
from .. helpers.commands import Commands
from .. helpers.rate import Difficulty
from .. models import CommentsModel
from .. objects.schemas import UploadComments, UploadPost
from .. services.user import UserService
from .. utils.crypt import base64_decode
from .. depends.posts import PostsModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import src.abstract.context as abc


def methods(cls):
    result = []
    for x, y in cls.__dict__.items():
        if type(y) == FunctionType and x.startswith("__") != True:
            result.append({"name": x, "func": y})
    return result


command_list = methods(Commands)


class CommentsService:

    def __init__(self, ctx: 'abc.AbstractContext'):
        self.ctx = ctx

    async def get_comments(self, level_id, page: int):
        comments = (
            (
                await self.ctx.database.comments.find_bySTMT(
                    select(CommentsModel)
                    .filter(CommentsModel.levelID == level_id)
                    .order_by(CommentsModel.id.desc())
                    .limit(system.page)
                    .offset(system.page * page)
                )
            )
            .all()
        )
        count = len(
            (
                await self.ctx.database.comments.find_byfield(CommentsModel.levelID == level_id)
            )
            .scalars()
            .all()
        )
        if comments is not None:
            return {"status": "ok", "database": comments, "count": count}
        else:
            return {"status": "error", "details": "comments not found"}

    async def upload_comments(self, data: UploadComments) -> dict:
        try:
            content = base64_decode(data.comment)
            print(content)
            if content.startswith("/"):
                await cls.commands_handler(
                    data=content[1:],
                    levelID=data.levelID,
                    authorID=data.accountID,
                )
                return {"status": "ok", "type": "command"}
            else:
                db_comment = CommentsModel(
                    authorId=data.accountID,
                    content=data.comment,
                    progress=data.percent,
                    levelID=data.levelID,
                    authorName=(
                        (await UserService().get_user_byid(data.accountID))
                    )["database"].userName,
                )
                await ctx.database.comments.add_one(db_comment)
                await ctx.commit()
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
            case "daily":
                day = datetime.date.today() + datetime.timedelta(days=1)
                model = models.FeaturedLevelsModel(type=1, levelid=levelID, onTime=day)
                db.add(model)
                await db.commit()
            case "weekly":
                day = datetime.date.today() + datetime.timedelta(days=1)
                model = models.FeaturedLevelsModel(type=2, levelid=levelID, onTime=day)
                db.add(model)
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

    def __init__(self, ctx: 'abc.AbstractContext'):
        self.ctx = ctx

    async def upload_post(self, data: UploadPost):
        async with self.ctx:
            db_post = PostsModel(
                accountID=data.accountID, content=data.content, timestamp=data.timestamp
            )
            self.ctx.console.info("Uploading post")
            await self.ctx.database.posts.add_one(db_post)
            await self.ctx.commit()
            return db_post

    async def delete_post(self, postID):
        db_level = (
            (await db.execute(select(PostsModel).filter(PostsModel.id == postID)))
            .scalars()
            .first()
        )
        await self.ctx.database.posts.find_byid(postID)
        await db.delete(db_level)
        await db.commit()

    async def get_post(self, usrid: int, page: int):
        offset = int(page) * 10
        stmt = select(PostsModel).filter(PostsModel.accountID == usrid)
        count = len(
            (await self.ctx.database.posts.find_bySTMT(stmt)).all()
        )
        stmt2 = select(PostsModel).filter(PostsModel.accountID == usrid).limit(10).offset(offset).order_by(
            PostsModel.id.desc()
        )
        return {
            "database": (
                (await self.ctx.database.posts.find_bySTMT(stmt2)).all()
            ),
            "count": count,
        }
