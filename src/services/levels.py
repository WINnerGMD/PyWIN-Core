from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np
from .. helpers.rate import Difficulty, Rate
from .. objects.schemas import UploadLevel
from .. schemas.levels.service.get import GetLevel
from .. models import LevelModel, GauntletsModel, MapPacksModel
from .. utils.gdform import formatted_date
from .. config import system
from .. schemas.levels.errors import *
from .. objects.levelObject import LevelObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. abstract import context as abc


class LevelService:

    def __init__(self, ctx: 'abc.AbstractContext'):
        self.ctx = ctx

    async def upload_level(self, data: UploadLevel):
        async with self.ctx:
            AuthorObj = await self.ctx.database.users.find_byid(data.accountID)
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
            await self.ctx.database.levels.add_one(db_lvl)
            await self.ctx.commit()
            return {"status": "ok", "level": db_lvl}

    # except Exception as e:
    #     return {"status": "error", "details": e}

    async def test_get_levels(self, data: GetLevel):
        async with self.ctx:
            page = data.page * system.page if data.page is not None else 0

            difficulty_mapping = {
                1: Difficulty.easy_Demon.value,
                2: Difficulty.medium_Demon.value,
                3: Difficulty.hard_Demon.value,
                4: Difficulty.insane_Demon.value,
                5: Difficulty.extreme_Demon.value
            }

            query = select(LevelModel)
            if data.difficulty is not None:
                match data.difficulty:
                    case Difficulty.gd_na:
                        query = query.where(LevelModel.difficulty == 0)
                    case Difficulty.gd_demon:
                        query = query.where(LevelModel.difficulty == difficulty_mapping.get(data.demonFilter, 6))
                    case _:
                        query = query.where(LevelModel.difficulty == Difficulty(data.difficulty).value)

            if isinstance(data.rate, tuple):
                query = query.where(LevelModel.rate > 0)
            elif data.rate == Rate.NoRate:
                query = query.where(LevelModel.rate >= 0)
            elif data.rate in [Rate.Feature, Rate.Epic]:
                query = query.where(LevelModel.rate == data.rate)

            match data.searchType:
                case 0:
                    query = query.where(LevelModel.name.like(f"%{data.string}%"))
                case 2:
                    query = query.order_by(LevelModel.likes.desc(), LevelModel.downloads.desc())
                case 4:
                    query = query.order_by(LevelModel.id.desc())
                case 5:
                    query = query.where(LevelModel.authorID == data.string)
                case 6:
                    query = query.where(LevelModel.rate == 1)
                case 11:
                    query = query.where(LevelModel.stars > 0)
                case 16:
                    query = query.where(LevelModel.rate >= 1)

            if data.lenght is not None:
                query = query.where(LevelModel.length == data.length)

            count = await self.ctx.database.levels.count()
            database = await self.ctx.database.levels.find_bySTMT(query.offset(page).limit(system.page))
            database = np.array(database.all()) if database else np.array([])

            if database.size:
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

    async def get_level_buid(self, levelID: int) -> LevelObject:
        try:
            levels = LevelObject(await self.ctx.database.levels.find_byfield(LevelModel.id == levelID), self.ctx)
            return levels
        except SQLAlchemyError as e:
            raise LevelNotFoundError

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
