from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.rate import Difficulty
from sql import models
from utils.crypt import xor_cipher, base64_encode, sha1_hash
from utils.gdform import gd_dict_str


class LevelObject:

    def __init__(self, service: models.Levels, db: AsyncSession):
        self.service = service
        self.db = db
        self.name = service.name
        pass

    def __str__(self) -> str:
        return str(self.service)

    async def rate(self, difficulty: Difficulty, stars: int = 0):
        pass

    async def like(self, accountID: int):
        if (await self.db.execute(select(models.Actions).filter(models.Actions.valueID == self.service.id,
                                                                models.Actions.accountID == accountID,
                                                                models.Actions.actionName == "Like"))).scalars().first() == None:
            query = update(models.Levels).filter(models.Levels.id == self.service.id).values(
                {"likes": models.Levels.likes + 1})
            await self.db.execute(query)
            await self.db.commit()

    async def __update_download_counter(self, level_id):
        query = update(models.Levels).filter(models.Levels.id == level_id).values(
            {"downloads": models.Levels.downloads + 1})
        await self.db.execute(query)
        await self.db.commit()

    async def downloadLevelHash1(self, levelString):
        hash = ""
        dataLen = len(levelString)
        divided = int(dataLen / 40)
        p = 0
        k = 0
        while k < dataLen:
            if p > 39: break
            hash += levelString[k]
            p += 1
            k = k + divided
        return await sha1_hash(hash, "xI25fpAapCQg")

    @staticmethod
    async def downloadLevelHash2(levelData):
        return await sha1_hash(levelData, "xI25fpAapCQg")

    async def GDDownload_level(self):

        level = self.service
        # info(f"Level download '{row.name}'")
        level_str = {
            1: level.id,
            2: level.name,
            3: level.desc,
            4: level.LevelString,
            5: level.version,
            6: level.authorID,
            8: 10,
            9: level.difficulty * 10 if level.difficulty != -3 else 0 ,
            10: level.downloads,
            12: level.AudioTrack,
            13: level.gameVersion,
            14: level.likes,
            15: level.lenght,
            17: 1 if level.difficulty >= 6 else 0,
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
            45: level.objects,
            27: f'{base64_encode(xor_cipher(str(level.password), "26364"))}#{await self.downloadLevelHash1(level.LevelString)}#' + await self.downloadLevelHash2(
                f'{level.authorID},{level.stars},{0},{level.id},{level.user_coins},{"1" if level.rate == 1 else "0"},{level.password},0'),


        }
        return (gd_dict_str(level_str))

    # return f'1:{row.id}:2:{row.name}:3:{row.desc}:4:{row.LevelString}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{"1" if row.rate == 1 else "0"}:42:{"1" if row.rate == 2 else "0"}:45:{row.objects}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:28:1 hour:29:1 hour:35:{row.song_id}:36::37:{row.coins}:38:{row.user_coins}:39:{0}:46::47::40:{row.is_ldm}:27:{base64_encode(xor_cipher(str(row.password), "26364"))}#{await self.downloadLevelHash1(row.LevelString)}#' + await self.downloadLevelHash2(
    #     f'{row.authorID},{row.stars},{0},{row.id},{row.user_coins},{"1" if row.rate == 1 else "0"},{row.password},0')


class LevelGroup:
    def __init__(self, service: models.Levels):
        self.service = service
        pass

    async def GDGet_level(self, page: int | None = 0, is_gauntlet: bool = False):
        levelsDataHash = ""
        levelData = []
        userString = ""
        for row in self.service['database']:
            feature = 0
            epic = 0
            if row.rate == 1:
                feature = 1
            elif row.rate == 2:
                epic = 1

            levelsDataHash += str(row.id)[0] + str(row.id)[-1] + str(row.stars) + str(row.user_coins)
            Level = gd_dict_str({
                1: row.id,
                2: row.name,
                3: row.desc,
                5: row.version,
                6: row.authorID,
                8: 10,
                9: row.difficulty * 10 if row.difficulty != -3 else 0,
                10: row.downloads,
                12: row.AudioTrack,
                13: row.gameVersion,
                14: row.likes,
                15: row.lenght,
                17: 0,
                18: row.stars,
                19: feature,
                25: 1 if row.difficulty == -3 else 0,
                27: 0,
                28: 0,
                29: 0,
                30: row.original,
                31: row.two_players,
                35: row.song_id,
                37: row.coins,
                38: row.user_coins,
                42: epic,
                43: 0,
                44: 1 if is_gauntlet == True else 0,
                45: row.objects
            })

            levelData.append(Level)
            # levelString += f'1:{row.id}:2:{row.name}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{feature}:42:{epic}:45:{row.objects}:3:{row.desc}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:37:{row.coins}:38:{row.user_coins}:39:{0}:46:1:47:2:35:{row.song_id}|'

            userString += f'{row.authorID}:{row.authorName}:{row.authorID}|'
        levelstr = '|'.join(levelData)
        return (
            f"{levelstr}#{userString}##{self.service['count']}:{page * 10}:10#{await sha1_hash(levelsDataHash, 'xI25fpAapCQg')}")
