import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Integer,
    String,
    Column,
    create_engine,
    ForeignKeyConstraint,
    UniqueConstraint,
    Float,
    Boolean,
)
from sqlalchemy_utils import database_exists, create_database

from log import logger

DATABASE = {
    "drivername": "postgresql",
    "host": "localhost",
    "port": "5432",
    "username": "postgres",
    "password": "qwerty",
    "database": "cats.db",
}
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}:{DATABASE["port"]}/{DATABASE["database"]}'
)

session = Session(bind=engine)


class BreedModel(Base):
    __tablename__ = "breeds"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    cats = relationship(
        "CatModel", back_populates="breed", cascade="all, delete-orphan"
    )


class CatModel(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    path_url = Column(String, nullable=False, unique=True)

    gender_male = Column(Boolean, nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    breed_id = Column(Integer, nullable=False)
    breed = relationship("BreedModel", back_populates="cats")

    __table_args__ = (
        ForeignKeyConstraint(["breed_id"], ["breeds.id"]),
        UniqueConstraint("name", "breed_id", "age"),
    )
