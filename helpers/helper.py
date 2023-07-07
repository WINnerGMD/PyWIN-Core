import json


def get_json():
    with open("./config.json","r") as json_file:
        return json.loads(json_file.read())
    
