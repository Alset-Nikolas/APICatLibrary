from models import BreedModel, session


def add_breed(new_breed: str) -> int:
    """
    Добавить новую породу кошки
    """
    br = BreedModel(name=new_breed)
    session.add(br)
    session.flush()
    session.commit()
    return br


def get_breed_by_name(name_bread) -> BreedModel:
    """
    По названию отдать id из бд
    """
    return session.query(BreedModel).filter(BreedModel.name == name_bread).first()


def create_if_not_exist(name_bread):
    """
    Добавим новую породу в бд, если такой нет
    """
    breed = get_breed_by_name(name_bread)
    if breed is None:
        breed = add_breed(name_bread)
    return breed.id
