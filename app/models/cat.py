import typing
from models import session, CatModel, BreedModel
import models.breed as models_breed
import dataclass.cat as obj
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import func, text, desc


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


def get_call_cat_query(param: typing.Dict) -> CatModel:
    """
    Создать запрос по всем котам, но не вызываем
    """
    rank_name = func.ts_rank(
        "{0.1,0.1,0.1,0.1}", CatModel.__ts_name__, func.to_tsquery(param["name"])
    )
    rank_age = func.ts_rank(
        "{0.1,0.1,0.1,0.1}", CatModel.__ts_name__, func.to_tsquery(str(param["age"]))
    )
    rank_desc = func.ts_rank(
        "{0.1,0.1,0.1,0.1}", CatModel.__ts_name__, func.to_tsquery(param["description"])
    )
    rank_breed = func.ts_rank(
        "{0.1,0.1,0.1,0.1}", BreedModel.__ts_vector__, func.to_tsquery(param["breed"])
    )
    rank = (
        func.coalesce(rank_name, 0)
        + func.coalesce(rank_age, 0)
        + func.coalesce(rank_desc, 0)
        + func.coalesce(rank_breed, 0)
    )
    return session.query(CatModel, rank.label("sum_rank")).join(
        BreedModel, BreedModel.id == CatModel.breed_id
    )


def add_sorted(query, sorted_key: str) -> Query:
    """
    Добавляем к запросу сортировку
    """
    print(query)
    if sorted_key == "default":
        return query.order_by(desc(text("sum_rank")))
    elif sorted_key == "age":
        return query.order_by(CatModel.age)
    elif sorted_key == "breed":
        return query.order_by(CatModel.breed_id)


def get_cats_by_filters(param: typing.Dict) -> typing.List[CatModel]:
    """
    Вернем всех котов, которые прошли фильтрацию
    """
    query: Query = get_call_cat_query(param)
    if param["name"]:
        query: Query = query.filter(
            CatModel.__ts_name__.match(param["name"], postgresql_regconfig="russian")
        )
    if param["age"]:
        query: Query = query.filter(
            CatModel.__ts_age__.match(str(param["age"]), postgresql_regconfig="russian")
        )
    if param["description"]:
        query: Query = query.filter(
            CatModel.__ts_description__.match(
                param["description"], postgresql_regconfig="russian"
            )
        )
    if param["breed"]:
        breeds: BreedModel = models_breed.search_breed_by_name(param["breed"])
        query: Query = query.filter(CatModel.breed_id.in_(breed.id for breed in breeds))
    query = add_sorted(query, param["sorted"])
    return [x[0] for x in query.all()]
