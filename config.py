import json

with open("config.json", 'r') as config:
    json = json.load(config)
    path = json["pywin"]['path']



print(path)