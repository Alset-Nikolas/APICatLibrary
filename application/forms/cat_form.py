from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

# from wtforms.validators import DataRequired


class CatForm(FlaskForm):
    name = StringField("name")
    breed = StringField("breed")
    age = IntegerField("age")
    description = StringField("description")
