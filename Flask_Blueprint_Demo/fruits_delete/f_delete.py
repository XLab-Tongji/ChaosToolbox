from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from fruits_data import FRUITS



fdel_blueprint = Blueprint("fdel_b",
                           __name__,
                           template_folder="template",
                           static_folder="static"
                           )


@fdel_blueprint.route("/f_delete/<int:fid>", methods=["GET", "POST"])
def f_delete(fid):
    for fruits in FRUITS:
        if fruits["id"] == fid:
            FRUITS.remove(fruits)

            pass
    return render_template("fruits_list.html", fruits=FRUITS)
