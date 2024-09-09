from pydantic import BaseModel
from src.helpers.rate import Difficulty, Rate
from src.objects.level.levelObject import LevelObject

class GetLevel(BaseModel):
    lenght: int | None
    gauntlet: int | None
    string: str | None
    searchType: int | None
    accountID: int | None
    difficulty: Difficulty | None
    demonFilter: int | None
    page: int | None
    rate: Rate | tuple | None
    coins: int | None
    song: int | None
    customSong: int | None


class GetLevelResponse(BaseModel):
    database: str
    count: int
