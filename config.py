import json

with open("config.json", 'r') as config:
    json = json.load(config)
    path = json["pywin"]['path']
    database = json["database"]
    use_win = json['system']['use_w']
    debug = json['system']['debug']
    pluginload = json['system']['pluginloader']