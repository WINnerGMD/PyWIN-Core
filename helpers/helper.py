import json
from database import db

def get_json():
    with open("./config.json","r") as json_file:
        return json.loads(json_file.read())
    
def get_user(id):
    return db(f"SELECT * FROM `users` WHERE `id` = '{id}'")[0]
