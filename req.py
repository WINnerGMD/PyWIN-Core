from functools import wraps

class Request:
    def __init__(self):
        pass
    
    def plugin(func):
        @wraps(func)
        def wrapper(*args):
            print("до")
            func(*args)
            print(func.__name__)
            print("после")
        return wrapper
    
    def pwreq(self,request):
        return request


obj = Request()
print(obj.pwreq("hello"))

@obj.plugin
def kick(printer):
    return "HELLo"

print(kick("efefef"))