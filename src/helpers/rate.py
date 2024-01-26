from enum import Enum


class Difficulty(Enum):
    gd_auto = -3
    gd_demon = -2
    gd_na = -1
    easy = 1
    normal = 2
    hard = 3
    harder = 4
    insane = 5
    easy_Demon = 7
    medium_Demon = 8
    hard_Demon = 6
    insane_Demon = 9
    extreme_Demon = 10


class Rate(Enum):
    NoRate = 0
    Feature = 1
    Epic = 2
    Legendary = 3
    GodLike = 4


