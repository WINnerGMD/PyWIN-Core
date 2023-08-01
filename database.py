from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import database
from sql import models

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{database["user"]}:{database["password"]}@{database["host"]}/{database["database"]}'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()