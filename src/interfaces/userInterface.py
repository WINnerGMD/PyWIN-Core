from .. models import LevelModel
from enum import Enum
from .. schemas.interface import InterfaceBaseSchema


class UserInterface:
    @staticmethod
    class Enums(Enum):
        id = 1
        name = 2
        description = 3
        version = 5
        authorID = 6
        difficultyDenum = 8  # 0 if is N/A level / 10 if level difficulty  is assigned
        difficultyNum = 9  # 0 -> N/A, 10 -> Easy, 20 -> Normal, 30 -> Hard, 40 -> Harder, 50 -> Insane
        downloads = 10
        OfficialAudio = 12
        gameVersion = 13
        likes = 14
        lenght = 15
        dislikes = 16
        demon = 17
        stars = 18
        isFeatured = 19

    def __init__(self, model, isGauntlet: bool) -> None:
        self._interface(model, isGauntlet)

    def items(self):
        return self.schema.items()

    @classmethod
    def __getitem__(cls, item) -> InterfaceBaseSchema:
        try:
            data = cls.Enums(item)
        except ValueError as e:
            raise KeyError("Invalid GDIndex")
        schema = InterfaceBaseSchema(
            GDIndex=data.value,
            Name=data.name
        )
        return schema

    def _interface(self, model, isGauntlet: bool):

        feature = 0
        epic = 0

        match model.rate:
            case 1:
                feature = 1
            case 2:
                epic = 1
            case 3:
                epic = 2
            case 4:
                epic = 3

        schema = {
            1: model.id,
            2: model.name,
            3: model.desc,
            5: model.version,
            6: model.authorID,
            8: 10,
            9: model.difficulty * 10 if model.difficulty != -3 else 0,
            10: model.downloads,
            12: model.AudioTrack,
            13: model.gameVersion,
            14: model.likes,
            15: model.lenght,
            17: 0,
            18: model.stars,
            19: feature,
            25: 1 if model.difficulty == -3 else 0,
            27: 0,
            28: 0,
            29: 0,
            30: model.original,
            31: model.two_players,
            35: model.song_id,
            37: model.coins,
            38: model.user_coins,
            39: 1,
            42: epic,
            43: 0,
            44: 1 if isGauntlet == True else 0,
            45: model.objects,
            47: 2
        }
        self.schema = schema
