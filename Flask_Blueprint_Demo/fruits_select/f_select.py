from flask import Blueprint
from flask import render_template
from fruits_data import FRUITS

fs_blueprint = Blueprint("fs_b",
                         __name__,
                         template_folder="template",
                         static_folder="static"
                         )


@fs_blueprint.route("/f_list")
def f_list():
    return render_template("fruits_list.html", fruits=FRUITS)
