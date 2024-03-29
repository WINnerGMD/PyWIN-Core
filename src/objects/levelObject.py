import numpy
import numpy as np
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.helpers.rate import Difficulty, Rate
from src.interfaces import UserInterface
from src.models import ActionsModel, LevelModel, UsersModel
from src.utils.crypt import xor_cipher, base64_encode, sha1_hash
from src.utils.gdform import gd_dict_str
from config import system
from typing import TYPE_CHECKING

# from services.comments import CommentsService
# from services.user import UserService

if TYPE_CHECKING:
    import src.abstract.context as abc


class LevelObject:
    def __init__(self, service: LevelModel, ctx: 'abc.AbstractContext'):
        self.service = service
        self.ctx = ctx

    def __str__(self) -> str:
        return str(self.service)

    async def user_rate(self, difficulty: Difficulty, stars: int, accountID: int):
        if (
                await self.db.execute(
                    select(ActionsModel).filter(
                        ActionsModel.accountID == accountID,
                        ActionsModel.level == self.service["database"].id,
                    )
                )
        ).scalars().first() is not None:
            return {
                "status": "error",
                "details": "the user has already done this action",
            }
        rate_model = ActionsModel(
            actionName="User Rate",
            value=stars,
            level=self.service["database"].id,
            accountID=accountID,
            data=str({"difficulty": difficulty.value, "stars": stars}),
        )
        self.db.add(rate_model)

        rates = (
            (
                await self.db.execute(
                    select(ActionsModel).filter(
                        ActionsModel.actionName == "User Rate",
                        ActionsModel.level == self.service["database"].id,
                    )
                )
            )
            .scalars()
            .all()
        )
        result = 0
        for i in rates:
            result += i.value

        result = result // len(rates)

        match result:
            case 1:
                difficulty = Difficulty.gd_auto
            case 2:
                difficulty = Difficulty.easy
            case 3:
                difficulty = Difficulty.normal
            case 4 | 5:
                difficulty = Difficulty.hard
            case 6 | 7:
                difficulty = Difficulty.harder
            case 8 | 9:
                difficulty = Difficulty.insane
            case 10:
                difficulty = Difficulty.easyDemon
        if difficulty == Difficulty.easyDemon and not system.demonRate:
            return {"status": "error", "details": "rate demon is false"}
        await self.db.execute(
            update(LevelModel)
            .filter(LevelModel.id == self.service["database"].id)
            .values({"difficulty": difficulty.value})
        )
        await self.db.commit()
        return {"status": "error"}

    async def rate(
            self, difficulty: Difficulty = None, stars: int = None, rate: Rate = None
    ):
        try:
            if difficulty is not None:
                if stars is not None:
                    if rate is not None:
                        modify_data = {
                            "difficulty": difficulty.value,
                            "stars": stars,
                            "rate": rate,
                        }
                    else:
                        modify_data = {"difficulty": difficulty.value, "stars": stars}
                else:
                    if rate is not None:
                        modify_data = {"difficulty": difficulty.value, "rate": rate}
            else:
                if stars is not None:
                    if rate is not None:
                        modify_data = {"stars": stars, "rate": rate}
                    else:
                        modify_data = {"stars": stars}
                else:
                    if rate is not None:
                        modify_data = {"rate": rate}

            match self.service["database"].rate:
                case 0:
                    cp = rate if rate is not None else 0
                case 1:
                    cp = rate - 1 if rate is not None else 0
                case 3:
                    cp = rate - 2 if rate is not None else 0
            print(cp)
            await self.db.execute(
                update(UsersModel)
                .filter(UsersModel.id == self.service["database"].authorID)
                .values({"cp": UsersModel.cp + cp})
            )

            request = (
                update(LevelsModel)
                .filter(LevelsModel.id == self.service["database"].id)
                .values(modify_data)
            )
            await self.db.execute(request)
            await self.db.commit()

            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "details": e}

    async def like(self, accountID: int):
        try:
            if (
                    await self.db.execute(
                        select(ActionsModel).filter(
                            ActionsModel.valueID == self.service["database"].id,
                            ActionsModel.accountID == accountID,
                            ActionsModel.actionName == "Like",
                        )
                    )
            ).scalars().first() is None:
                query = (
                    update(LevelsModel)
                    .filter(LevelsModel.id == self.service["database"].id)
                    .values({"likes": LevelsModel.likes + 1})
                )
                await self.db.execute(query)
                await self.db.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "details": e}

    async def dislike(self, accountID: int):
        try:
            if (
                    await self.db.execute(
                        select(ActionsModel).filter(
                            ActionsModel.valueID == self.service["database"].id,
                            ActionsModel.accountID == accountID,
                            ActionsModel.actionName == "Like",
                        )
                    )
            ).scalars().first() is None:
                query = (
                    update(LevelsModel)
                    .filter(LevelsModel.id == self.service["database"].id)
                    .values({"likes": LevelsModel.likes - 1})
                )
                await self.db.execute(query)
                await self.db.commit()
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "details": e}

    @staticmethod
    async def downloadLevelHash1(level):
        data = ""
        l = len(level) // 40
        for i in range(40):
            data += level[i * l]
        return await sha1_hash(
            data,
            "xI25fpAapCQg",
        )

    # async def GDGet_comments(self, page):
    #     comments_object = await CommentsService().get_comments(
    #         db=self.db, level_id=self.services["database"].id
    #     )
    #     comment_dict = []
    #     for i in comments_object:
    #         userObject = await UserService().get_user_byid(db=self.db, id=i.authorId)
    #         iconkits = userObject.iconkits
    #         comment_dict
    #         comment_string += f"2~{i.content}~3~{i.authorId}~4~{i.likes}~7~{i.is_spam}~10~{i.progress}~9~2 minutes~6~31468976:1~{i.authorName}~9~{iconkits['accIcon']}~10~{iconkits['color1']}~11~{iconkits['color2']}~14~0~15~0~16~{i.authorId}|"
    #     return comment_string + "#5705:2:10"

    async def GDDownload_level(self, is_featured: bool):
        level = self.service.first()
        # info(f"Level download '{row.name}'")
        featured_id = 0
        if is_featured:
            var = 0 if level.id == -1 else 1
            featured_id = 6
        level_str = {
            1: level.id,
            2: level.name,
            3: level.desc,
            4: level.LevelString,
            5: level.version,
            6: level.authorID,
            8: 10,
            9: level.difficulty * 10 if level.difficulty != -3 else 0,
            10: level.downloads,
            12: level.AudioTrack,
            13: level.gameVersion,
            14: level.likes,
            15: level.lenght,
            17: 0,
            18: level.stars,
            19: 1 if level.rate == 1 else 0,
            25: 1 if level.difficulty == -3 else 0,
            28: "1 hour",
            29: "1 hour",
            30: level.original,
            31: level.two_players,
            37: level.coins,
            38: level.user_coins,
            40: level.is_ldm,
            42: 1 if level.rate == 2 else 0,
            43: "",
            45: level.objects,
            27: f'{base64_encode(xor_cipher(str(level.password), "26364"))}',
        }

        if is_featured:
            user_info = f"#{level.authorID}:{level.authorName}:{level.authorID}"
            level_str.update({41: 6})
            answer = (
                    "#".join(
                        (
                            gd_dict_str(level_str),
                            await self.downloadLevelHash1(level.LevelString),
                            await sha1_hash(
                                f'{level.authorID},{level.stars},{0},{level.id},{level.user_coins},{"1" if level.rate == 1 else "0"},{level.password},{featured_id}',
                                "xI25fpAapCQg",
                            ),
                        )
                    )
                    + user_info
            )
        else:
            answer = "#".join(
                (
                    gd_dict_str(level_str),
                    await self.downloadLevelHash1(level.LevelString),
                    await sha1_hash(
                        f'{level.authorID},{level.stars},{0},{level.id},{level.user_coins},{"1" if level.rate == 1 else "0"},{level.password},{featured_id}',
                        "xI25fpAapCQg",
                    ),
                )
            )
        await self.ctx.database.levels.update(level.id, {"downloads": level.downloads + 1})
        return answer


class LevelGroup:
    def __init__(self, service: LevelModel):
        self.service = service
        pass

    async def GDGet_level(self, page: numpy.uint8 | None = 0, is_gauntlet: bool = False):
        levelsDataHash = ""
        levelData = np.array([])
        userString = ""
        for row in self.service['database']:
            # Fuck Robtop
            levelsDataHash += (
                    str(row.id)[0] + str(row.id)[-1] + str(row.stars) + str(row.user_coins)
            )
            Level = gd_dict_str(interface := UserInterface(row, is_gauntlet))
            levelData = numpy.append(levelData, Level)
            userString += f"{row.authorID}:{row.authorName}:{row.authorID}|"
        levelstr = "|".join(levelData)
        return f"{levelstr}#{userString}##{self.service['count']}:{page * system.page}:{system.page}#{await sha1_hash(levelsDataHash, 'xI25fpAapCQg')}"
