from typing import Iterable, Self, List


class GDObject:
    name = "not implemented"

    def __str__(self) -> str:
        return self.name

    async def render(self) -> str:
        raise NotImplementedError

    def __repr__(self):
        return "<class 'GDObject'>"


class GDList(List[GDObject]):
    V = GDObject

    def __init__(self, *args: V | list) -> None:
        result = []
        for arg in args:
            if isinstance(arg, self.V):
                result.append(arg)
            elif isinstance(arg, Iterable) and all(isinstance(i, self.V) for i in arg):
                result.extend(arg)
            else:
                raise TypeError("GDList can only contain objects of type GDObject")

        super().__init__(result)

    def __str__(self):
        return "GDList:: < | " + super().__repr__()[1:-1] + " | >"  # Fun

    def __repr__(self):
        return "<class 'GDList'>"

    def render(self) -> str:
        raise NotImplementedError

    def __setitem__(self, index: int, value: V) -> None:
        if isinstance(value, GDObject):
            super().__setitem__(index, value)
        else:
            raise TypeError("GDObjectList can only contain objects of type GDObject")


# part fix circular import in python
def GDObjectRadd(self, other: GDObject | GDList) -> GDList:
    if isinstance(other, GDList):
        other.append(self)
        return other
    elif isinstance(other, GDObject):
        return GDList([self, other])
    else:
        raise TypeError(f"incorrect type {len(other)}")


def GDObjectAdd(self, other: GDObject | GDList) -> GDList:
    if isinstance(other, GDList):
        other.append(self)
        return other
    elif isinstance(other, GDObject):
        return GDList([self, other])
    else:
        raise TypeError(f"incorrect type {len(other)}")


GDObject.__radd__ = GDObjectRadd
GDObject.__add__ = GDObjectAdd
