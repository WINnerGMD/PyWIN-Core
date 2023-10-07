from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.rate import Difficulty, Rate
from objects.schemas import UploadLevel, GetLevel
from services.user import UserService
from sql import models
from utils.gdform import formatted_date
from config import system

class LevelService:
    @staticmethod
    async def upload_level(db: AsyncSession, data: UploadLevel):
            AuthorObj = (await UserService().get_user_byid(db=db, id=data.accountID))
            upload_time = formatted_date()
            if AuthorObj['status'] == 'ok':
                db_lvl = models.Levels(
                    name=data.levelName,
                    desc=data.levelDesc,
                    version=data.levelVersion,
                    authorID=data.accountID,
                    authorName=AuthorObj['database'].userName,
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
                db.add(db_lvl)
                await db.commit()
                await db.refresh(db_lvl)

                return {"status": "ok", "level": db_lvl}
            else:
                return {"status": "error", "details": 'user not found'}
        # except Exception as e:
        #     return {"status": "error", "details": e}

    @staticmethod
    async def get_levels(db: AsyncSession, data: GetLevel):
        try:
            if data.page is not None:
                page = data.page * 10
            difficulty = data.difficulty
            if difficulty == -1:
                difficulty = 0
            elif difficulty == -2:
                match data.demonFilter:
                    case 1:
                        difficulty = Difficulty.easyDemon
                    case 2:
                        difficulty = Difficulty().mediumDemon
                    case 3:
                        difficulty = Difficulty.hardDemon
                    case 4:
                        difficulty = Difficulty.insaneDemon
                    case 5:
                        difficulty = Difficulty.extremeDemon
            result = select(models.Levels).filter(
                models.Levels.coins > 0
                if data.coins == "1"
                else models.Levels.coins >= 0,
                models.Levels.lenght >= 0
                if data.lenght == "-"
                else models.Levels.lenght == data.lenght,
                models.Levels.difficulty >= -3
                if data.difficulty is None
                else models.Levels.difficulty == difficulty,
                models.Levels.difficulty > 5
                if data.demonFilter is None
                else models.Levels.difficulty < 0,
                models.Levels.rate == 2
                if data.epic == 1
                else models.Levels.rate >= 0,
                models.Levels.rate == 1
                if data.featured == 1
                else models.Levels.rate >= 0,
                models.Levels.id <= 76
                if data.gauntlet == 1
                else models.Levels.id >= 0,
            )
            count = len((await db.execute(result)).scalars().all())
            match data.searchType:
                case 0:
                    answer = (
                        (
                            await db.execute(
                                result.filter(
                                    models.Levels.name.like(f"%{data.string}%")
                                )
                                .order_by(
                                    models.Levels.likes.desc(),
                                    models.Levels.downloads.desc(),
                                )
                                .offset(page)
                                .limit(10)
                            )
                        )
                        .scalars()
                        .all()
                    )
                    if answer != []:
                        database = answer
                    else:
                        database = (
                            (
                                await db.execute(
                                    result.filter(models.Levels.id == data.str)
                                )
                            )
                            .scalars()
                            .all()
                        )
                case 2:
                    database = (
                        (
                            await db.execute(
                                result.order_by(
                                    models.Levels.likes.desc(),
                                    models.Levels.downloads.desc(),
                                )
                                .offset(page)
                                .limit(10)
                            )
                        )
                        .scalars()
                        .all()
                    )
                case 4:
                    database = (
                        (
                            await db.execute(
                                result.order_by(models.Levels.id.desc())
                                .limit(10)
                                .offset(page)
                            )
                        )
                        .scalars()
                        .all()
                    )
                case 5:
                    database = (
                        (
                            await db.execute(
                                result.filter(models.Levels.authorID == data.string)
                            )
                        )
                        .scalars()
                        .all()
                    )
                case 6:
                    database = (
                        (await db.execute(result.filter(models.Levels.rate == 1)))
                        .scalars()
                        .all()
                    )
                case 11:
                    database = (
                        (
                            await db.execute(
                                result.filter(models.Levels.stars > 0)
                                .limit(10)
                                .offset(page)
                            )
                        )
                        .scalars()
                        .all()
                    )
                case 16:
                    database = (
                        (await db.execute(result.filter(models.Levels.rate >= 1)))
                        .scalars()
                        .all()
                    )
                case _:
                    database = (await db.execute(result)).scalars().all()

            if database != []:
                return {"status": "ok", "database": database, "count": count}
            else:
                return {
                    "status": "error",
                    "details": f"Level Not Found '{data.string}'",
                }
        except Exception as e:
            return {"status": "error", "details": e}

    @staticmethod
    async def test_get_levels(db: AsyncSession, data: GetLevel):
        try:
            if data.page != None:
                page = data.page * system.page
            else:
                page = 0

            difficulty = data.difficulty
            if difficulty == -1:
                difficulty = 0
            elif difficulty == -2:
                match data.demonFilter:
                    case 1:
                        difficulty = Difficulty.easyDemon.value
                    case 2:
                        difficulty = Difficulty.mediumDemon.value
                    case 3:
                        difficulty = Difficulty.hardDemon.value
                    case 4:
                        difficulty = Difficulty.insaneDemon.value
                    case 5:
                        difficulty = Difficulty.extremeDemon.value

            "fuck"
            result = select(models.Levels)

            if data.difficulty != None:
                match data.difficulty.value:
                    case -1:
                        result = result.filter(models.Levels.difficulty == 0)
                    case -2:
                        match data.demonFilter:
                            case 1:
                                difficulty = Difficulty.easyDemon.value
                                result = result.filter(
                                    models.Levels.difficulty == difficulty
                                )
                            case 2:
                                difficulty = Difficulty.mediumDemon.value
                                result = result.filter(
                                    models.Levels.difficulty == difficulty
                                )
                            case 3:
                                difficulty = Difficulty.hardDemon.value
                                result = result.filter(
                                    models.Levels.difficulty == difficulty
                                )
                            case 4:
                                difficulty = Difficulty.insaneDemon.value
                                result = result.filter(
                                    models.Levels.difficulty == difficulty
                                )
                            case 5:
                                difficulty = Difficulty.extremeDemon.value
                                result = result.filter(
                                    models.Levels.difficulty == difficulty
                                )
                            case _:
                                result = result.filter(models.Levels.difficulty > 5)
                    case _:
                        result = result.filter(
                            models.Levels.difficulty
                            == Difficulty(data.difficulty).value
                        )
            match data.rate:
                case Rate.NoRate:
                    result = result.filter(models.Levels.rate >= 0)
                case Rate.Feature:
                    result = result.filter(models.Levels.rate == 1)
                case Rate.Epic:
                    result = result.filter(models.Levels.rate == 2)
                case tuple:
                    result = result.filter(models.Levels.rate > 0)



            match data.searchType:
                case 0:
                    result = (

                            result.filter(
                                models.Levels.name.like(f"%{data.string}%")
                            )
                            .order_by(
                                models.Levels.likes.desc(),
                                models.Levels.downloads.desc(),
                            )
                    )
                case 2:
                    result = (
                            result.order_by(
                                models.Levels.likes.desc(),
                                models.Levels.downloads.desc(),
                                )
                    )
                case 4:
                    result = (
                            result.order_by(models.Levels.id.desc())
                    )
                case 5:
                    result = (
                            result.filter(models.Levels.authorID == data.string)
                    )
                case 6:
                    result = (
                        (
                            result.filter(models.Levels.rate == 1)
                        )
                    )
                case 11:
                    result = (
                            result.filter(models.Levels.stars > 0)
                    )
                case 16:
                    result = (
                            result.filter(models.Levels.rate >= 1)
                    )

            count = len((await db.execute(result)).scalars().all())
            database = (await db.execute(result.offset(page).limit(system.page))).scalars().all()
            if database != []:
                return {"status": "ok", "database": database, "count": count}
            else:
                return {
                    "status": "error",
                    "details": f"Level Not Found '{data.string}'",
                }
        except Exception as e:
            return {"status": "error", "details": e}

    @staticmethod
    async def get_levels_group(db: AsyncSession, levels: list):
        try:
            print(levels)
            query = select(models.Levels).filter(models.Levels.id.in_(levels))
            levelgroup = (await db.execute(query)).scalars().all()
            if levelgroup != []:
                count = len(levelgroup)
                return {"status": "ok", "database": levelgroup, "count": count}
            else:
                return {"status": "error", "details": "level group not found"}
        except Exception as e:
            return {"status": "ok", "details": e}

    @staticmethod
    async def get_gauntlets_levels(db: AsyncSession, indexpack: int):
        try:
            query1 = select(models.Gauntlets.levels).filter(
                models.Gauntlets.indexpack == indexpack
            )
            levels = (await db.execute(query1)).scalars().first()
            query2 = select(models.Levels).filter(
                models.Levels.id.in_(levels.split(","))
            )
            levelpack = (await db.execute(query2)).scalars().all()
            return {"status": "ok", "database": levelpack, "count": 1}
        except:
            return

    @staticmethod
    async def get_map_packs(db: AsyncSession, page: int):
        query = select(models.MapPacks)
        count = len((await db.execute(query)).scalars().all())
        database = (await db.execute(query.limit(10).offset(page * 10))).scalars().all()
        return {"database": database, "count": count}

    @staticmethod
    async def get_level_buid(levelID, db: AsyncSession):
        levels = (
            (
                await db.execute(
                    select(models.Levels).filter(models.Levels.id == levelID)
                )
            )
            .scalars()
            .first()
        )
        if levels is not None:
            return {"status": "ok", "database": levels}
        else:
            return {"status": "error", "details": "level not found"}

    @staticmethod
    async def get_total_levels(db: AsyncSession):
        try:
            query = select(models.Levels)
            total = len((await db.execute(query)).scalars().all())
            return {"status": "ok", "count": total}
        except Exception as e:
            return {"status": "error", "details": e}

    @staticmethod
    async def delete_level(levelID, db: AsyncSession):
        db_level = (
            (
                await db.execute(
                    select(models.Levels).filter(models.Levels.id == levelID)
                )
            )
            .scalars()
            .first()
        )
        await db.delete(db_level)
        await db.commit()
