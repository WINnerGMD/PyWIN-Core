from pydantic import BaseModel


class LevelSchema(BaseModel):
    id: int
    name: str
    desc: str
    version: int
    authorID: int
    AuthorName: str
    gameVersion: int
    likes: int
    downloads: int
    AudioTrack: int
    song_id: int
    lenght: int
    stars: int
    coins: int
    difficulty: int
    user_coins: int
    rate: int
    original: int
    two_players: int
    is_ldm: bool
    objects: int
    password: int
    LevelString: str
