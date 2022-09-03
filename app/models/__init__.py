from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import (
    Integer,
    String,
    Column,
    create_engine,
    ForeignKeyConstraint,
    UniqueConstraint,
    Boolean,
    func,
    cast,
    Index,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.operators import op

DATABASE = {
    "drivername": "postgresql",
    "host": "postgres",
    "port": "5432",
    "username": "postgres",
    "password": "qwerty",
    "database": "db_cats",
}
Base = declarative_base()
engine = create_engine(
    f'postgresql+psycopg2://{DATABASE["username"]}:{DATABASE["password"]}@{DATABASE["host"]}:{DATABASE["port"]}/{DATABASE["database"]}'
)


session = Session(bind=engine)


def create_tsvector_1(*args):
    exp = args[0]
    for e in args[1:]:
        exp += " " + e
    return func.to_tsvector("russian", exp)


CONFIG = "russian"


def create_tsvector(*args):
    field, weight = args[0]
    exp = func.setweight(func.to_tsvector(CONFIG, field), weight)
    for field, weight in args[1:]:
        exp = op(exp, "||", func.setweight(func.to_tsvector(CONFIG, field), weight))
    return exp


class BreedModel(Base):
    __tablename__ = "breeds"
    # __searchable__ = ["name"]

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    cats = relationship(
        "CatModel", back_populates="breed", cascade="all, delete-orphan"
    )

    __ts_vector__ = create_tsvector(
        (cast(func.coalesce(name, ""), postgresql.TEXT), "A")
    )
    __table_args__ = (Index("idx_breed_fts", __ts_vector__, postgresql_using="gin"),)


class CatModel(Base):
    __tablename__ = "cats"
    # __searchable__ = ["name", "age", "description"]
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    path_url = Column(String, nullable=False, unique=True)

    gender_male = Column(Boolean, nullable=False)
    age = Column(Integer, nullable=False)
    description = Column(String, nullable=False)

    breed_id = Column(Integer, nullable=False)
    breed = relationship("BreedModel", back_populates="cats")

    __ts_name__ = create_tsvector(
        (cast(func.coalesce(name, ""), postgresql.TEXT), "A"),
    )
    __ts_age__ = create_tsvector((cast(func.coalesce(age, 0), postgresql.TEXT), "B"))

    __ts_description__ = create_tsvector(
        (cast(func.coalesce(description, ""), postgresql.TEXT), "C")
    )

    __table_args__ = (
        ForeignKeyConstraint(["breed_id"], ["breeds.id"]),
        UniqueConstraint("name", "breed_id", "age"),
        Index(
            "idx_cat_name_fts",
            __ts_name__,
            postgresql_using="gin",
        ),
        Index(
            "idx_cat_desc_fts",
            __ts_description__,
            postgresql_using="gin",
        ),
        Index(
            "idx_cat_age_fts",
            __ts_age__,
            postgresql_using="gin",
        ),
    )
