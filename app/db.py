from multiprocessing.util import LOGGER_NAME
from sqlalchemy_utils import database_exists, create_database, drop_database
from log import logger
from models import Base, engine
import settings
import models.cat as cat_models
from dataclass.cat import Cat


def fill_db():
    """
    Заполним бд котятами
    """
    for cat_dit in settings.CATS:
        cat_obj: Cat = Cat.create_cat_obj_for_dict(cat_dit)
        cat_models.add_cat(cat_obj)


def init_db() -> None:
    """
    Создаем таблицы
    """
    # drop_database(engine.url)

    logger.info("init data base")
    if not database_exists(engine.url):
        logger.info("create db cats.db")
        create_database(engine.url)
        Base.metadata.create_all(engine)
        fill_db()
        return
    logger.info("cats.db exist")
