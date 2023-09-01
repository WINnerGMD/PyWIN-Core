from utils.security import base64_decode
from sql import models

class LevelObject:

    def __init__(self,service: models.Levels):
        self.service = service
        pass

    def name(self):
        return self.service.name
    
    async def desc(self):
        return base64_decode(self.service.desc)
    




