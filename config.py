import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv


load_dotenv('.env')
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
        with open('./config.json', 'r') as config:
            json_object = json.load(config)
            if json_object['use_env']:
                parsedb = {
                    'host': os.environ.get("POSTGRES_HOST"),
                    'port': os.environ.get("POSTGRES_PORT"),
                    'user': os.environ.get("POSTGRES_NAME"),
                    'password': os.environ.get("POSTGRES_PASSWORD"),
                    'database': os.environ.get("POSTGRES_DB")
                }
                parseredis = {
                    'port': os.environ.get('REDIS_PORT'),
                    'ttl': os.environ.get('REDIS_TTL')
                }
                database = Database(**parsedb)
                redis = Redis(**parseredis)
                system = System(**json_object['system'])
                return {'database': database, 'system': system, 'redis': redis}
            else:
                database = Database(**json_object['database'])
                system = System(**json_object['system'])
                redis = Redis(**json_object['redis'])
                return {'database': database, 'system': system, 'redis': redis}
    except KeyError as ex:
        print(ex)

    except FileNotFoundError as ex:
        print(ex)

conf = parse_config()

database = conf['database']
system = conf['system']
redis = conf['redis']
