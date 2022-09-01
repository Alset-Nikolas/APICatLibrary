from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField

from wtforms.validators import DataRequired, ValidationError, Optional


def age_is_real(form, field):
    if field.data:
        if field.data < 0:
            raise ValidationError("Возраст >= 0")


def name_is_real(form, field):
    print(field.data.isupper())
    if field.data:
        if not field.data[0].isupper():
            raise ValidationError("Имя с заглавной буквы ")


class CatForm(FlaskForm):
    name = StringField("name", validators=[name_is_real])
    breed = StringField("breed")
    age = IntegerField("age", default=0, validators=[Optional(), age_is_real])
    description = StringField("description")

    sorted = StringField("sorted")
