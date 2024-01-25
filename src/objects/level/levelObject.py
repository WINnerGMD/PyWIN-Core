import numpy

from src.interfaces import UserInterface
from src.objects.GDObject import GDObject
import numpy as np
from src.models import LevelModel
from src.utils.crypt import sha1_hash
from src.utils.gdform import gd_dict_str


class LevelObject(GDObject):
    name = "Level"

    def __init__(self, database: LevelModel, count: int = 1) -> None:
        self.database = database
        self.count = count

    def __len__(self) -> str:
        return self.database.lenght

    async def render(self, is_gauntlet: bool = False):
        levelsDataHash = ""
        levelData = np.array([])
        userString = ""
        for row in self.service['database']:
            # Fuck Robtop
            levelsDataHash += (
                    str(row.id)[0] + str(row.id)[-1] + str(row.stars) + str(row.user_coins)
            )
            Level = gd_dict_str(interface := UserInterface(row, is_gauntlet))
            print(interface[5])
            levelData = numpy.append(levelData, Level)
            userString += f"{row.authorID}:{row.authorName}:{row.authorID}|"
        levelstr = "|".join(levelData)
        return f"{levelstr}#{userString}##{self.service['count']}:{page * system.page}:{system.page}#{await sha1_hash(levelsDataHash, 'xI25fpAapCQg')}"
