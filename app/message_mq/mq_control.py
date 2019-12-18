from flask import Blueprint,jsonify
from flask import request
from flask import abort

from services.message_queue import RabbitMq

rabbitmq = Blueprint('rabbitmq', __name__)


@rabbitmq.route('/tool/api/v1.0/rabbitmq/control', methods=['POST'])
def mq_control():
    if not request.json or 'open' not in request.json:
        abort(400)
    return jsonify(RabbitMq.mq_control(request.json['open']))


@rabbitmq.route('/tool/api/v1.0/rabbitmq/delete', methods=['POST'])
def mq_delete():
    if not request.json or 'queue' not in request.json:
        abort(400)
    return jsonify(RabbitMq.clear_all_messages(request.json['queue']))


@rabbitmq.route('/tool/api/v1.0/rabbitmq/get_message', methods=['GET'])
def get_message():
    return jsonify(RabbitMq.consumer())
