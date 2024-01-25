from typing import Annotated
from fastapi import Depends

from src.context import UoWContext, AbstractContext

Context = Annotated[AbstractContext, Depends(UoWContext)]
