from flask import Flask, render_template
import models.cat as cat_models
import db
from forms.cat_form import CatForm, FlaskForm
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
csrf = CSRFProtect(app)


@app.route("/", methods=["GET", "POST"])
def main_rout():
    form: FlaskForm = CatForm()

    if form.validate_on_submit():

        return (
            render_template(
                "main.html", cats=cat_models.get_cats_by_filters(form.data), form=form
            ),
            200,
        )
    return render_template("main.html", cats=cat_models.get_all_cat(), form=form), 200


@app.route("/cat-<int:id>", methods=["GET"])
def cat_info_route(id):
    form: FlaskForm = CatForm()
    cat_obj = cat_models.get_cat_by_id(id)
    return render_template("cat_info.html", form=form, cat=cat_obj)


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
