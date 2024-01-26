from .. helpers.rate import Difficulty
from .. objects.levelObject import LevelObject


class Commands:
    def __init__(self, permissions=None, user=None, level: LevelObject = None):
        self.__permissions = permissions
        self.__user = user
        self.__level = level

    def rate(self, difficulty: Difficulty = None, stars: int = None):
        if self.__level is not None:
            if self.__permissions is not None:
                if self.__permissions.rateLevels == True:
                    if self.__user is not None:
                        "TODO: Action add"
                        result = self.__level.rate(difficulty=difficulty, stars=stars)
                        info(result)
                    else:
                        return {"status": "error", "details": "user empty"}
                else:
                    return {
                        "status": "error",
                        "details": "permissions denied(rateLevels)",
                    }
            else:
                return {"status": "error", "details": "permission empty"}
        else:
            return {"status": "error", "details": "permission empty"}
