import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from .depends.logs import Console

load_dotenv(".env")


class Shards(BaseModel):
    fire: bool
    ice: bool
    poison: bool
    shadow: bool
    lava: bool


class SmallChest(BaseModel):
    max_mana: int
    min_mana: int
    max_diamonds: int
    min_diamonds: int
    shards: Shards


class Database(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str


class System(BaseModel):
    pluginloader: bool
    auto_verified: bool
    use_asade: bool
    debug: bool
    default_role: int
    page: int
    demonRate: int
    leaderboards_limit: int
    lang: str
    path: str


class Redis(BaseModel):
    port: int
    ttl: int


def parse_config():
    try:
        with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as config:
            json_object = json.load(config)
            if json_object["use_env"]:
                parsedb = {
                    "host": os.environ.get("POSTGRES_HOST"),
                    "port": os.environ.get("POSTGRES_PORT"),
                    "user": os.environ.get("POSTGRES_NAME"),
                    "password": os.environ.get("POSTGRES_PASSWORD"),
                    "database": os.environ.get("POSTGRES_DB"),
                }
                parseredis = {
                    "port": os.environ.get("REDIS_PORT"),
                    "ttl": os.environ.get("REDIS_TTL"),
                }

                database = Database(**parsedb)
                redis = Redis(**parseredis)
                system = System(**json_object["system"])
                return {"database": database, "system": system, "redis": redis}
            else:
                smallchest_parse = json_object['chests']['small']
                bigchest_parse = json_object['chests']['big']
                chest_small = SmallChest(max_mana=smallchest_parse['max_mana'],
                                         min_mana=smallchest_parse['min_mana'],
                                         max_diamonds=smallchest_parse['min_mana'],
                                         min_diamonds=smallchest_parse['min_mana'],
                                         shards=Shards(fire=smallchest_parse["shards"]["fire"],
                                                       ice=smallchest_parse["shards"]["ice"],
                                                       poison=smallchest_parse["shards"]["poison"],
                                                       shadow=smallchest_parse["shards"]["shadow"],
                                                       lava=smallchest_parse["shards"]["lava"], )

                                         )
                chest_big = SmallChest(max_mana=bigchest_parse['max_mana'],
                                       min_mana=bigchest_parse['min_mana'],
                                       max_diamonds=bigchest_parse['min_mana'],
                                       min_diamonds=bigchest_parse['min_mana'],
                                       shards=Shards(fire=bigchest_parse["shards"]["fire"],
                                                     ice=bigchest_parse["shards"]["ice"],
                                                     poison=bigchest_parse["shards"]["poison"],
                                                     shadow=bigchest_parse["shards"]["shadow"],
                                                     lava=bigchest_parse["shards"]["lava"], )
                                       )

                database = Database(**json_object["database"])
                system = System(**json_object["system"])
                redis = Redis(**json_object["redis"])
                return {"database": database, "system": system, "redis": redis, "small_chest": chest_small,
                        "big_chest": chest_big}
    except KeyError as ex:
        print(ex)

    except FileNotFoundError as ex:
        print(ex)
    except Exception as ex:
        print("ex")


conf = parse_config()

database = conf["database"]
system = conf["system"]
redis = conf["redis"]
small_chest = conf["small_chest"]
big_chest = conf["big_chest"]


# class ConfigEdit():
#     __slots__ = ("database", "system", "redis", "social")
#
#     def __init__(self):
#         pass
#
#     def __enter__(self):
#         with open(os.path.join(os.path.dirname(__file__), "config.json"), "a") as file:
#             self.file = file
#             self.config = json.loads(file.read())
#         return self
#
#     def __setattr__(self, key, value):
#         try:
#             self.config[key] = value
#         except Exception as ex:
#             pass
#
#     def __getattr__(self, key: str) -> int | str:
#         print("suka")
#         try:
#             return self.config[key]
#         except Exception as ex:
#             pass
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if exc_type is None:
#             self.write(self.config)
#         else:
#             Console.alert("Error on config editing")
#
#     @staticmethod
#     def open() -> dict:
#         with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as file:
#             json_data = json.loads(file.read())
#             Console.info(f"Opened config file")
#         return json_data
#
#     @staticmethod
#     def write(config: dict) -> None:
#         with open(os.path.join(os.path.dirname(__file__), "config.json"), "w") as file:
#             Console.info(f"Edited config file")
#             file.write(json.dumps(config, indent=4))
