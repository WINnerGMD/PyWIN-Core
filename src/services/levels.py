import numpy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np
from src.helpers.rate import Difficulty, Rate
from src.objects.schemas import UploadLevel
from src.schemas.levels.service.get import GetLevel
from src.depends.user import UsersRepository
from src.models import LevelModel, GauntletsModel, MapPacksModel
from src.utils.gdform import formatted_date
from config import system
from src.depends.level import LevelsRepository
from src.schemas.levels.errors import *


class LevelService:
    @staticmethod
    async def upload_level(data: UploadLevel):
        AuthorObj = await UsersRepository().find_byid(data.accountID)
        upload_time = formatted_date()
        db_lvl = LevelModel(
            name=data.levelName,
            desc=data.levelDesc,
            version=data.levelVersion,
            authorID=data.accountID,
            authorName=AuthorObj.userName,
            gameVersion=data.gameVersion,
            AudioTrack=data.audioTrack,
            lenght=data.levelLength,
            coins=data.coins,
            user_coins=0,
            original=data.original,
            two_players=data.twoPlayer,
            song_id=data.songID,
            is_ldm=data.ldm,
            password=data.password,
            upload_date=upload_time,
            LevelString=data.levelString,
        )
        await LevelsRepository.add_one(db_lvl)

        return {"status": "ok", "level": db_lvl}

    # except Exception as e:
    #     return {"status": "error", "details": e}


    @staticmethod
    async def test_get_levels(data: GetLevel):
            if data.page is not None:
                page = data.page * system.page
            else:
                page = 0

            if (difficulty := data.difficulty) == -1:
                difficulty = 0
            elif difficulty == -2:
                match data.demonFilter:
                    case 1:
                        difficulty = Difficulty.easy_Demon.value
                    case 2:
                        difficulty = Difficulty.medium_Demon.value
                    case 3:
                        difficulty = Difficulty.hard_Demon.value
                    case 4:
                        difficulty = Difficulty.insane_Demon.value
                    case 5:
                        difficulty = Difficulty.extreme_Demon.value

            "fuck"
            result = select(LevelModel)

            if data.difficulty != None:
                match data.difficulty.value:
                    case -1:
                        result = result.filter(LevelModel.difficulty == 0)
                    case -2:
                        match data.demonFilter:
                            case 1:
                                difficulty = Difficulty.easy_Demon.value
                                result = result.filter(
                                    LevelModel.difficulty == difficulty
                                )
                            case 2:
                                difficulty = Difficulty.medium_Demon.value
                                result = result.filter(
                                    LevelModel.difficulty == difficulty
                                )
                            case 3:
                                difficulty = Difficulty.hard_Demon.value
                                result = result.filter(
                                    LevelModel.difficulty == difficulty
                                )
                            case 4:
                                difficulty = Difficulty.insane_Demon.value
                                result = result.filter(
                                    LevelModel.difficulty == difficulty
                                )
                            case 5:
                                difficulty = Difficulty.extremeDemon.value
                                result = result.filter(
                                    LevelModel.difficulty == difficulty
                                )
                            case _:
                                result = result.filter(LevelModel.difficulty > 5)
                    case _:
                        result = result.filter(
                            LevelModel.difficulty == Difficulty(data.difficulty).value
                        )
            match data.rate:
                case Rate.NoRate:
                    result = result.filter(LevelModel.rate >= 0)
                case Rate.Feature:
                    result = result.filter(LevelModel.rate == 1)
                case Rate.Epic:
                    result = result.filter(LevelModel.rate == 2)
                case tuple:
                    result = result.filter(LevelModel.rate > 0)

            match data.searchType:
                case 0:
                    result = result.filter(
                        LevelModel.name.like(f"%{data.string}%")
                    ).order_by(
                        LevelModel.likes.desc(),
                        LevelModel.downloads.desc(),
                    )
                case 2:
                    result = result.order_by(
                        LevelModel.likes.desc(),
                        LevelModel.downloads.desc(),
                    )
                case 4:
                    result = result.order_by(LevelModel.id.desc())
                case 5:
                    result = result.filter(LevelModel.authorID == data.string)
                case 6:
                    result = result.filter(LevelModel.rate == 1)
                case 11:
                    result = result.filter(LevelModel.stars > 0)
                case 16:
                    result = result.filter(LevelModel.rate >= 1)

            count = len(await LevelsRepository.find_all())
            database = np.array((await LevelsRepository.find_bySTMT(result.offset(page).limit(system.page))).scalars().all())
            if database.size is not 0:
                return {"status": "ok", "database": database, "count": count}
            else:
                raise LevelNotFoundError

    @staticmethod
    async def get_levels_group(db: AsyncSession, levels: list):
        try:
            print(levels)
            query = select(LevelModel).filter(LevelModel.id.in_(levels))
            levelgroup = (await db.execute(query)).scalars().all()
            if levelgroup != []:
                count = len(levelgroup)
                return {"status": "ok", "database": levelgroup, "count": count}
            else:
                return {"status": "error", "details": "level group not found"}
        except Exception as e:
            return {"status": "ok", "details": e}

    @staticmethod
    async def get_gauntlets_levels(indexpack: int):
        try:
            query1 = select(GauntletsModel.levels).filter(
                GauntletsModel.indexpack == indexpack
            )
            levels = await LevelsRepository.findfirst_bySTMT(query1)
            print(levels)
            query2 = select(LevelModel).filter(LevelModel.id.in_(levels.split(",")))
            levelpack = await LevelsRepository.findall_bySTMT(query2)
            return {"status": "ok", "database": levelpack, "count": 1}
        except Exception as e:
            print(e)
            return

    @staticmethod
    async def get_map_packs(db: AsyncSession, page: int):
        query = select(MapPacksModel)
        count = len((await db.execute(query)).scalars().all())
        database = (await db.execute(query.limit(10).offset(page * 10))).scalars().all()
        return {"database": database, "count": count}

    @staticmethod
    async def get_level_buid(levelID):
        levels = await LevelsRepository().find_byfield(LevelModel.id == levelID)
        if levels is not None:
            return {"status": "ok", "database": levels}
        else:
            return {"status": "error", "details": "level not found"}

    @staticmethod
    async def get_total_levels(db: AsyncSession):
        try:
            query = select(LevelModel)
            total = len((await db.execute(query)).scalars().all())
            return {"status": "ok", "count": total}
        except Exception as e:
            return {"status": "error", "details": e}

    @staticmethod
    async def delete_level(levelID, db: AsyncSession):
        db_level = (
            (await db.execute(select(LevelModel).filter(LevelModel.id == levelID)))
            .scalars()
            .first()
        )
        await db.delete(db_level)
        await db.commit()
