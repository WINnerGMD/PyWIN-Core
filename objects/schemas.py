from pydantic import BaseModel
from helpers.rate import Difficulty, Rate


class UpdateStats(BaseModel):
    id: int
    stars: int
    demons: int
    diamonds: int
    coins: int
    usr_coins: int
    iconkits: dict



class UploadLevel(BaseModel):
    levelString: str
    accountID: int
    levelName: str
    levelDesc: str
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


class GetLevel(BaseModel):
    lenght: int | None
    gauntlet: int | None
    string: str | None
    searchType: int
    accountID: int | None
    difficulty: Difficulty | None
    demonFilter: int | None
    page: int
    rate: Rate | tuple | None
    coins: int
    song: int | None
    customSong: int | None



class UploadComments(BaseModel):
    userName: str
    accountID: int
    comment: str
    levelID: int
    percent: int



class UploadPost(BaseModel):
    accountID: int
    content: str
    timestamp: str



class GetPost(BaseModel):
    accountID: int



class RateLevel(BaseModel):
    id: int
    rate: int
    stars: int
    difficulty: int



class likeItem(BaseModel):
    itemID: int
    type: int
    like: int
    accountID: int


class LikeUpload(BaseModel):
    likes: int


class DownloadItem(BaseModel):
    downloads: int
