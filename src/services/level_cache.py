from dataclasses import dataclass
from typing import Optional
from sqlalchemy import select
from database import async_session_maker
from src.models import LevelModel


@dataclass
class LevelMeta:
    id: int
    name: str
    desc: str
    version: str
    authorID: int
    authorName: str
    gameVersion: int
    likes: int
    downloads: int
    AudioTrack: int
    lenght: int
    stars: int
    difficulty: int
    coins: int
    user_coins: int
    rate: int
    original: int
    two_players: int
    song_id: int
    is_ldm: int
    objects: int
    password: int


class LevelCache:
    _instance: Optional["LevelCache"] = None
    _levels: dict[int, LevelMeta] = {}
    _loaded: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    async def load_all(self) -> int:
        async with async_session_maker() as session:
            stmt = select(
                LevelModel.id,
                LevelModel.name,
                LevelModel.desc,
                LevelModel.version,
                LevelModel.authorID,
                LevelModel.authorName,
                LevelModel.gameVersion,
                LevelModel.likes,
                LevelModel.downloads,
                LevelModel.AudioTrack,
                LevelModel.lenght,
                LevelModel.stars,
                LevelModel.difficulty,
                LevelModel.coins,
                LevelModel.user_coins,
                LevelModel.rate,
                LevelModel.original,
                LevelModel.two_players,
                LevelModel.song_id,
                LevelModel.is_ldm,
                LevelModel.objects,
                LevelModel.password,
            )
            result = await session.execute(stmt)
            rows = result.all()
            
            self._levels.clear()
            for row in rows:
                meta = LevelMeta(
                    id=row.id,
                    name=row.name,
                    desc=row.desc,
                    version=row.version,
                    authorID=row.authorID,
                    authorName=row.authorName,
                    gameVersion=row.gameVersion,
                    likes=row.likes,
                    downloads=row.downloads,
                    AudioTrack=row.AudioTrack,
                    lenght=row.lenght,
                    stars=row.stars,
                    difficulty=row.difficulty,
                    coins=row.coins,
                    user_coins=row.user_coins,
                    rate=row.rate,
                    original=row.original,
                    two_players=row.two_players,
                    song_id=row.song_id,
                    is_ldm=row.is_ldm,
                    objects=row.objects,
                    password=row.password,
                )
                self._levels[row.id] = meta
            
            self._loaded = True
            return len(self._levels)

    def get_by_id(self, level_id: int) -> Optional[LevelMeta]:
        return self._levels.get(level_id)

    def search(
        self,
        name: Optional[str] = None,
        difficulty: Optional[int] = None,
        rate: Optional[int] = None,
        page: int = 0,
        limit: int = 10,
    ) -> tuple[list[LevelMeta], int]:
        results = list(self._levels.values())
        
        if name:
            name_lower = name.lower()
            results = [l for l in results if name_lower in l.name.lower()]
        
        if difficulty is not None:
            results = [l for l in results if l.difficulty == difficulty]
        
        if rate is not None:
            results = [l for l in results if l.rate == rate]
        
        total = len(results)
        start = page * limit
        end = start + limit
        
        return results[start:end], total

    def invalidate(self, level_id: int) -> None:
        self._levels.pop(level_id, None)

    async def reload_one(self, level_id: int) -> Optional[LevelMeta]:
        async with async_session_maker() as session:
            stmt = select(
                LevelModel.id,
                LevelModel.name,
                LevelModel.desc,
                LevelModel.version,
                LevelModel.authorID,
                LevelModel.authorName,
                LevelModel.gameVersion,
                LevelModel.likes,
                LevelModel.downloads,
                LevelModel.AudioTrack,
                LevelModel.lenght,
                LevelModel.stars,
                LevelModel.difficulty,
                LevelModel.coins,
                LevelModel.user_coins,
                LevelModel.rate,
                LevelModel.original,
                LevelModel.two_players,
                LevelModel.song_id,
                LevelModel.is_ldm,
                LevelModel.objects,
                LevelModel.password,
            ).where(LevelModel.id == level_id)
            
            result = await session.execute(stmt)
            row = result.first()
            
            if row is None:
                self._levels.pop(level_id, None)
                return None
            
            meta = LevelMeta(
                id=row.id,
                name=row.name,
                desc=row.desc,
                version=row.version,
                authorID=row.authorID,
                authorName=row.authorName,
                gameVersion=row.gameVersion,
                likes=row.likes,
                downloads=row.downloads,
                AudioTrack=row.AudioTrack,
                lenght=row.lenght,
                stars=row.stars,
                difficulty=row.difficulty,
                coins=row.coins,
                user_coins=row.user_coins,
                rate=row.rate,
                original=row.original,
                two_players=row.two_players,
                song_id=row.song_id,
                is_ldm=row.is_ldm,
                objects=row.objects,
                password=row.password,
            )
            self._levels[level_id] = meta
            return meta

    def count(self) -> int:
        return len(self._levels)


level_cache = LevelCache()
