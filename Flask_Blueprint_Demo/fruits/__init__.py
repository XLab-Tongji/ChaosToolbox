from flask import Flask
from fruits_select import f_select
from fruits_add import f_add
from fruits_update import f_update
from fruits_delete import f_delete


def create_fruits_app():
    fruits_app = Flask(__name__)
    fruits_app.register_blueprint(f_select.fs_blueprint)
    fruits_app.register_blueprint(f_add.fa_blueprint)
    fruits_app.register_blueprint(f_update.fup_blueprint)
    fruits_app.register_blueprint(f_delete.fdel_blueprint)
    return fruits_app
