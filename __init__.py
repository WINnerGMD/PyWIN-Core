"""Here i going to make setup functions"""
import json
import os


def settings(name: str, srvid: int, password: str):
    with open(os.path.join(os.path.dirname(__file__), "src/config.json"), "w") as file:
        data = {
            "database": {
                "host": "localhost",
                "port": 3306,
                "user": f"gdps_{srvid}",
                "password": password,
                "database": "pywinbd"
            },
            "redis": {
                "port": 6379,
                "ttl": 10
            },
            "logger": {
                "info": True,
                "warning": True,
                "error": True
            },
            "social": {
                "GDPS_name": name
            },
            "system": {
                "pluginloader": True,
                "auto_verified": True,
                "use_asade": True,
                "debug": True,
                "default_role": 1,
                "page": 5,
                "demonRate": 0,
                "leaderboards_limit": 5,
                "lang": "en",
                "path": "/winnertestss"
            },
            "json:api": {
                "isWorked": True,
                "path": "/v2"
            },
            "gd:api": {
                "isWorked": True,
                "path": "/database"
            },
            "musix": {
                "use_musix": False,
                "musix_token": "",
                "asade_connect": False
            },
            "chests": {
                "small": {
                    "max_mana": 100,
                    "min_mana": 20,
                    "max_diamonds": 1,
                    "min_diamonds": 0,
                    "shards": {
                        "fire": True,
                        "ice": True,
                        "poison": True,
                        "shadow": True,
                        "lava": True
                    }
                },
                "big": {
                    "max_mana": 500,
                    "min_mana": 50,
                    "max_diamonds": 3,
                    "min_diamonds": 0,
                    "shards": {
                        "fire": True,
                        "ice": True,
                        "poison": True,
                        "shadow": True,
                        "lava": True
                    }

                }
            },
            "asade": {
                "token": "...",
                "verifed_users": 1
            },

            "danger": {
                "default-salt": ""

            },
            "use_env": False,
            "db": "MySQL"
        }
        json_string = json.dumps(data, indent=4)
        file.write(json_string)
