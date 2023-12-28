from pydantic import BaseModel
from src.helpers.rate import Rate, Difficulty

class StatsSchema(BaseModel):
    stars: int
    likes: int
    downloads: int
    coins: int
    objects: int
    user_coins: bool


class APILevelSchema(BaseModel):
    id: int
    name: str
    desc: str
    version: int
    authorID: int
    AuthorName: str
    gameVersion: int
    AudioTrack: int
    song_id: int
    lenght: int
    two_players: bool
    is_ldm: bool
    difficulty: str
    rate: str
    stats: StatsSchema
