
class SQLAlchemyNotFound(Exception):
    def __init__(self):
        self.message = "SQLAlchemyNotFound"
        super().__init__("SQLAlchemyNotFound")
