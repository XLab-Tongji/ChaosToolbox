from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from fruits_data import FRUITS

fup_blueprint = Blueprint("fup_b",
                          __name__,
                          template_folder="template",
                          static_folder="static"
                          )


@fup_blueprint.route("/f_update/<int:fid>", methods=["GET", "POST"])
def fruits_update(fid):
    if request.method == "POST":
        fruits_id = int(request.form["id"])
        fruits_dic = {
            "id": fruits_id,
            "name": request.form["name"],
            "price": int(request.form["price"])
        }
        for index, fruits in enumerate(FRUITS):
            if fruits["id"] == fruits_id:
                FRUITS[index] = fruits_dic
        return redirect("/f_list")
    for fruits in FRUITS:
        if fruits["id"] == fid:
            return render_template("fruits_update.html", fruits=fruits)

    return render_template("fruits_update.html", fruits="")
