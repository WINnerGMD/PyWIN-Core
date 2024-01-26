from ... depends.logs import Console


class LevelNotFoundError(Exception):
    def __init__(self, message=None):
        Console.alert("Level not Found")
        self.message = message
        super().__init__(message)
