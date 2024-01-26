from pydantic import BaseModel
from .... helpers.rate import Difficulty, Rate


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
