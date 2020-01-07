import sys

sys.path.append('')

from flask import Flask, jsonify
from common_options import get_info
from chaosblade import chaosblade
from influxdb_and_prometheus import get_data
from message_mq import mq_control
from flask_httpauth import HTTPBasicAuth
from utils.config import Config
from flask import make_response

auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.get_password
def get_password(username):
    if username == Config.user_name:
        return Config.password
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


app.register_blueprint(get_info.get_info)
app.register_blueprint(chaosblade.chaosblade)
app.register_blueprint(get_data.get_data)
app.register_blueprint(mq_control.rabbitmq)
