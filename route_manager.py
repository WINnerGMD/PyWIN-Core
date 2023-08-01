from fastapi import HTTPException
from fastapi import APIRouter
import inspect
import json
import random
from config import debug

router = APIRouter()
        
route_config = []
plugins = []
def plugin_management(pluginname):
    if debug == True:
        print(f"plugin {pluginname} setup")
    plugins.append(pluginname)
edit_access = False


# route_config_sh().get_route({'hello': 'sds'})
def error_message():
    raise HTTPException(status_code=200, detail="plugin system close connection")

def default_route():
    if edit_access == True:
        def wrapper(func):
            route_config.append({func.__name__:func})
            vartds = [func,error_message]
            return random.choice(vartds)
        return wrapper

    def wrapper(func):
        return func
    return wrapper


def route_manager():
    def wrapper(func):
        pass
    
    return wrapper


@route_manager()
def message():
    return "hello world"

