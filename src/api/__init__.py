from fastapi import FastAPI
from .levels.get_levels import router as get_levels

app = FastAPI(
    title="PyWIN Core API Doc",
    docs_url="/swagger",
    version='2.0'
)


app.include_router(get_levels)

