from flask import Blueprint, jsonify
from flask import request
from services.fault_injector import FaultInjector
from flask import abort

stress_inject = Blueprint('stress_inject', __name__)


@stress_inject.route('/tool/api/v1.0/stress/inject', methods=['POST'])
def inject():
    if not request.json or not 'type' in request.json \
            or not 'duration' in request.json \
            or not 'host' in request.json:
        abort(400)
    dto = {
        'type': request.json['type'],
        'inject_duration': request.json['duration'],
        'host': request.json['host']
    }
    if dto['type'] == 'cpu':
        return jsonify(FaultInjector.inject_cpu(dto))
    elif dto['type'] == 'mem':
        return jsonify(FaultInjector.inject_mem(dto))
    else:
        return jsonify(FaultInjector.inject_io(dto))
