from typing import Iterable, Self, List
# import src.objects.GDList as GDList

# GDList = GDList.GDList
class GDObject:
    name = "not implemented"

    def __str__(self) -> str:
        return self.name

    async def render(self) -> str:
        raise NotImplementedError

    def __repr__(self):
        return "<class 'GDObject'>"

    # part fix circular import in python
    # def __radd__(self, other: Self | GDList) -> GDList:
    #     if isinstance(other, GDList):
    #         other.append(self)
    #         return other
    #     elif isinstance(other, GDObject):
    #         return GDList([self, other])
    #     else:
    #         raise TypeError(f"incorrect type {len(other)}")
    #
    # def __add__(self, other: Self | GDList) -> GDList:
    #     if isinstance(other, GDList):
    #         other.append(self)
    #         return other
    #     elif isinstance(other, GDObject):
    #         return GDList([self, other])
    #     else:
    #         raise TypeError(f"incorrect type {len(other)}")
