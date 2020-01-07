from flask import request, abort
from flask import Blueprint, jsonify
from services.influxdb_observer import InfluxdbObserver
from services.prometheus_observer import PrometheusObserver

get_data = Blueprint('get_data', __name__)


@get_data.route('/tool/api/v1.0/get_measurements', methods=['POST'])
def get_measurements():
    if not request.json or 'database' not in request.json:
        abort(400)
    return jsonify(InfluxdbObserver.select_measurements(request.json['database']))


@get_data.route('/tool/api/v1.0/get_values', methods=['POST'])
def get_values():
    if not request.json or 'database' not in request.json \
            or 'measurement' not in request.json or 'start_time' not in request.json or 'end_time' not in request.json:
        abort(400)
    return jsonify(InfluxdbObserver.select_measurements_values(
        request.json['database'], request.json['measurement'], request.json['start_time'], request.json['end_time']))


@get_data.route('/tool/api/v1.0/get_sock_performance', methods=['POST'])
def get_sock_performance():
    if not request.json or 'start' not in request.json or 'end' not in request.json:
        abort(400)
    dto = {
        "start": request.json['start'],
        "end": request.json['end']
    }
    return jsonify(PrometheusObserver.sock_performance_picker(dto))
