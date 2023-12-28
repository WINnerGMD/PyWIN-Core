from enum import IntEnum

from pydantic import BaseModel
from src.helpers.rate import Difficulty, Rate
from dataclasses import dataclass
from datetime import datetime


class DailyChestType(IntEnum):
    SMALL = 0
    LARGE = 1


@dataclass
class DailyChest:
    id: int
    user_id: int
    type: DailyChestType
    mana: int
    diamonds: int
    fire_shards: int
    ice_shards: int
    poison_shards: int
    shadow_shards: int
    lava_shards: int
    demon_keys: int
    claimed_ts: datetime


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
