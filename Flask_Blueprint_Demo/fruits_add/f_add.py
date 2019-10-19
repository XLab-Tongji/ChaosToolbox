from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from fruits_data import FRUITS

fa_blueprint = Blueprint("fa_b",
                         __name__,
                         template_folder="template",
                         static_folder="static"
                         )


@fa_blueprint.route("/f_add", methods=["GET", "POST"])
def fruits_add():
    if request.method == "POST":
        fruits_dic = {
            "id": request.form["id"],
            "name": request.form["name"],
            "price": request.form["price"]
        }
        FRUITS.append(fruits_dic)
        return render_template("fruits_list.html", fruits=FRUITS)
    return render_template("fruits_add.html")
