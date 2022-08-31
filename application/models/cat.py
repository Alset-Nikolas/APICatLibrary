from models import session, CatModel, BreedModel
import models.breed as models_breed
import dataclass.cat as obj


def get_cat(name: str, age: int, breed: str):
    bread = models_breed.get_breed_by_name(breed)
    # todo like %desc%
    return (
        session.query(CatModel)
        .filter(CatModel.name == name)
        .filter(CatModel.age == age)
        .filter(CatModel.breed_id == bread.id)
        .first()
    )


def add_cat(cat: obj.Cat):
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


def get_all_cat():
    return (
        session.query(CatModel)
        .join(BreedModel, BreedModel.id == CatModel.breed_id)
        .all()
    )


def filter_by_breed(breed):
    return session.query(CatModel).filter(CatModel.breed == breed)


def filter_by_name(name):
    return session.query(CatModel).filter(CatModel.name == name)


def filter_by_age(age):
    return session.query(CatModel).filter(CatModel.age == age)


def filter_by_desc(desc):
    return session.query(CatModel).filter(CatModel.description.like(f"%{desc}%"))


def get_all_cats_sort_by_breed():
    return session.query(CatModel).order_by(CatModel.breed).all()


def get_all_cats_sort_by_age():
    return session.query(CatModel).order_by(CatModel.age).all()


def get_cats_by_filters():
    pass
