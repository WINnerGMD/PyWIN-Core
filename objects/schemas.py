from dataclasses import dataclass
from pydantic import BaseModel

class UpdateStats(BaseModel):
    id: int
    stars: int
    demons: int
    diamonds: int
    coins: int
    usr_coins: int
    iconkits: dict


@dataclass
class UploadLevel:
    levelString: str
    accountID: int
    levelName: str 
    # levelDesc: str
    levelVersion: int
    levelLength: int
    audioTrack: int
    password: str 
    original: int
    twoPlayer: int
    songID: str  
    objects: int 
    coins: int 
    requestedStars: int
    ldm: int
    gameVersion: int




@dataclass
class GetLevel:
    lenght: int
    str: str 
    type: int 
    accountID: int
    difficulty: int
    demonFilter: int
    page : int
    featured: int
    epic: int
    coins: int
    song: int
    customSong: int


@dataclass
class UploadComments:
    userName: str
    accountID: int
    comment: str
    levelID: int
    percent: int