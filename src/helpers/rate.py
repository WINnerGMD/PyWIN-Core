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
    easyDemon = 7
    mediumDemon = 8
    hardDemon = 6
    insaneDemon = 9
    extremeDemon = 10


class Rate(Enum):
    NoRate = 0
    Feature = 1
    Epic = 2
    Legendary = 3
    GodLike = 4


print(Difficulty.easy.value)
