from dataclasses import dataclass


@dataclass
class Cat:
    name: str
    path_url: str
    gender_male: bool
    age: int
    description: str
    breed: str

    @staticmethod
    def create_cat_obj_for_row(row):
        return Cat(
            name=row[0],
            path_url=row[1],
            gender_male=row[2],
            age=row[3],
            description=row[4],
            breed=row[5],
        )

    @staticmethod
    def create_cat_obj_for_dict(dict_cat):
        return Cat(
            name=dict_cat["name"],
            path_url=dict_cat["path_url"],
            gender_male=dict_cat["gender_male"],
            age=dict_cat["age"],
            description=dict_cat["description"],
            breed=dict_cat["breed"],
        )
