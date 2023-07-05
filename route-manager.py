from plugins.origins import app
import inspect



def route_sys():
    def wrapper(func):
        print(func.__name__)
    return wrapper



@route_sys()
def hui():
    print("load")