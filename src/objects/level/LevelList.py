from .. GDList import GDList


class LevelList(GDList):
    def render(self, page: int | None = 0, is_gauntlet: bool = False):
        levelsDataHash = ""
        levelData = tuple()
        userString = ""
        for row in self.service['database']:
            # Fuck Robtop
            levelsDataHash += (
                    str(row.id)[0] + str(row.id)[-1] + str(row.stars) + str(row.user_coins)
            )
            Level = gd_dict_str(interface := UserInterface(row, is_gauntlet))
            levelData = numpy.append(levelData, Level)
            userString += f"{row.authorID}:{row.authorName}:{row.authorID}|"
        levelstr = "|".join(levelData)
        return f"{levelstr}#{userString}##{self.service['count']}:{page * system.page}:{system.page}#{await sha1_hash(levelsDataHash, 'xI25fpAapCQg')}"