from flask import Flask, render_template, request
import models.cat as cat_models
import db
from forms.cat_form import CatForm, FlaskForm
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)


@app.route("/", methods=["GET", "POST"])
def main_rout():
    form: FlaskForm = CatForm()
    if form.validate():
        return (
            render_template("main.html", cats=cat_models.get_all_cat(), form=form),
            200,
        )
    return render_template("main.html", cats=cat_models.get_all_cat(), form=form), 200


@app.route("/<name>/<age>/<breed>", methods=["GET"])
def cat_info_route(name, age, breed):
    return f"name={name}, age={age}, breed={breed}"


if __name__ == "__main__":
    db.init_db()
    app.run(debug=False)
