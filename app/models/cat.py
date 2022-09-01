import typing
from models import session, CatModel, BreedModel
import models.breed as models_breed
import dataclass.cat as obj
from sqlalchemy.orm.query import Query


def get_cat_by_id(id: int) -> CatModel:
    """
    По id кота вернем обьект кота
    """
    return session.query(CatModel).filter(CatModel.id == id).first()


def add_cat(cat: obj.Cat) -> int:
    """
    Добавить нового котика
    """
    breed_id = models_breed.create_if_not_exist(cat.breed)
    new_cat = CatModel(
        name=cat.name,
        path_url=cat.path_url,
        gender_male=cat.gender_male,
        age=cat.age,
        description=cat.description,
        breed_id=breed_id,
    )
    session.add(new_cat)
    session.commit()
    return new_cat.id


def get_all_cat() -> typing.List[CatModel]:
    """
    Отдать всех котов из бд
    """
    return (
        session.query(CatModel)
        .join(BreedModel, BreedModel.id == CatModel.breed_id)
        .all()
    )


def get_call_cat_query() -> CatModel:
    """
    Создать запрос по всем котам, но не вызываем
    """
    return session.query(CatModel).join(BreedModel, BreedModel.id == CatModel.breed_id)


def add_sorted(query, sorted_key: str) -> Query:
    """
    Добавляем к запросу сортировку
    """
    if sorted_key == "default":
        return query.order_by(CatModel.id)
    elif sorted_key == "age":
        return query.order_by(CatModel.age)
    elif sorted_key == "breed":
        return query.order_by(BreedModel.name)


def get_cats_by_filters(param: typing.Dict) -> typing.List[CatModel]:
    """
    Вернем всех котов, которые прошли фильтрацию
    """
    query: Query = get_call_cat_query()
    if param["name"]:
        query: Query = query.filter(CatModel.name == param["name"])
    if param["age"]:
        query: Query = query.filter(CatModel.age == param["age"])
    if param["description"]:
        query: Query = query.filter(
            CatModel.description.like(f"%{param['description']}%")
        )
    if param["breed"]:
        breed: BreedModel = models_breed.get_breed_by_name(param["breed"])
        if breed:
            query: Query = query.filter(CatModel.breed_id == breed.id)
        else:
            return []
    query = add_sorted(query, param["sorted"])
    return query.all()
