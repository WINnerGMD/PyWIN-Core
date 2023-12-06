from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
)

from database import Base


class MusixModel(Base):
    __tablename__ = "musix"