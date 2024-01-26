from src.objects.GDObject import GDObject, GDList


class UserObject(GDObject):
    name = "User Object"


class UserList(GDList):
    V = UserObject
