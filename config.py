import json

with open("config.json", 'r') as config:
    json = json.load(config)
    path = json["pywin"]['path']
    database = json["database"]
    use_win = json['system']['use_w']
    debug = json['system']['debug']
    pluginload = json['system']['pluginloader']
    default_role = json['system']['default_role']
    redis_port = json['redis']['port']
    redis_ttl = json['redis']['ttl']

    logger_info = json['logger']['info']
    logger_warning = json['logger']['warning']
    logger_error = json['logger']['error']


"TODO: make normal config handler bruh"