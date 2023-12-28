from fastapi import FastAPI
from .levels.get_levels import router as get_levels
from .users.get_users import router as get_users
app = FastAPI(
    title="PyWIN Core API Doc",
    docs_url="/swagger",
    version='2.0'
)


app.include_router(get_levels)
app.include_router(get_users)
