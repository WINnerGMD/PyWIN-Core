from utils.crypt import base64_decode
from utils.gdform import gd_dict_str
from sql import models
from helpers.rate import Difficulty
import hashlib
from utils.crypt import chechValid,xor_cipher,base64_encode, sha1_hash
from logger import info
class LevelObject:

    def __init__(self,service: models.Levels):
        self.service = service
        self.name = service.name
        pass
    
    async def rate(self, difficulty: Difficulty, stars: int = 0):
        pass

    async def downloadLevelHash1(self,levelString):
        hash = ""
        dataLen = len(levelString)
        divided = int(dataLen/40)
        p = 0
        k = 0
        while k < dataLen:
            if p > 39: break
            hash += levelString[k]
            p+=1
            k = k + divided
        return await sha1_hash(hash,"xI25fpAapCQg")

    async def downloadLevelHash2(self, levelData):
        return await sha1_hash(levelData,"xI25fpAapCQg")
    
    async def GDDownload_level(self):
        row = self.service
        info(f"Level download '{row.name}'")
        return f'1:{row.id}:2:{row.name}:3:{row.desc}:4:{row.LevelString}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{"1" if row.rate == 1 else "0"}:42:{"1" if row.rate == 2 else "0"}:45:{row.objects}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:28:1 hour:29:1 hour:35:{row.song_id}:36::37:{row.coins}:38:{row.user_coins}:39:{0}:46::47::40:{row.is_ldm}:27:{base64_encode(xor_cipher(str(row.password), "26364"))}#{await self.downloadLevelHash1(row.LevelString)}#' + await self.downloadLevelHash2(f'{row.authorID},{row.stars},{0},{row.id},{row.user_coins},{"1" if row.rate == 1 else "0"},{row.password},0')
    
class LevelGroup:
    def __init__(self, service: models.Levels):
        self.service = service
        pass
    
    async def GDGet_level(self, page:int):
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

            levelsDataHash += str(row.id)[0]+str(row.id)[-1]+str(row.stars)+str(row.user_coins)
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
                45: row.objects
            })

            levelData.append(Level)
            # levelString += f'1:{row.id}:2:{row.name}:5:{row.version}:6:{row.authorID}:8:10:9:{row.difficulty}0:10:{row.downloads}:12:{row.AudioTrack}:13:{row.gameVersion}:14:{row.likes}:17:{0}:43:{0}:25:{0}:18:{row.stars}:19:{feature}:42:{epic}:45:{row.objects}:3:{row.desc}:15:{row.lenght}:30:{row.original}:31:{row.two_players}:37:{row.coins}:38:{row.user_coins}:39:{0}:46:1:47:2:35:{row.song_id}|'

            userString += f'{row.authorID}:{row.authorName}:{row.authorID}|'
        levelstr = '|'.join(levelData)
        return ( f"{levelstr}#{userString}##{self.service['count']}:{page*10}:10#{await sha1_hash(levelsDataHash, 'xI25fpAapCQg')}")
    

    
        
        
        





