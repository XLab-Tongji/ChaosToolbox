from flask import Blueprint, jsonify
from flask import request
from flask import abort
from services.fault_injector import FaultInjector

chaosblade = Blueprint('chaosblade', __name__)


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-cpu', methods=['POST'])
def chaos_inject_cpu():
    if not request.json or 'host' not in request.json:
        abort(400)
    dto = {
        'host': request.json['host'],
    }
    return jsonify(FaultInjector.chaos_inject_cpu(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-mem', methods=['POST'])
def chaos_inject_mem():
    if not request.json or 'host' not in request.json or 'percent' not in request.json:
        abort(400)
    dto = {
        'host': request.json['host'],
        'percent': request.json['percent']
    }
    return jsonify(FaultInjector.chaos_inject_mem(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-disk', methods=['POST'])
def chaos_inject_disk():
    if not request.json or 'host' not in request.json or 'type' not in request.json:
        abort(400)
    dto = {
        'host': request.json['host'],
        'type': request.json['type']
    }
    return jsonify(FaultInjector.chaos_inject_disk(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-network', methods=['POST'])
def chaos_inject_network():
    if not request.json or 'host' not in request.json or 'time' not in request.json or 'timeout' not in request.json:
        abort(400)
    dto = {
        'host': request.json['host'],
        'time': request.json['time'],
        'timeout': request.json['timeout']
    }
    return jsonify(FaultInjector.chaos_inject_network(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/inject-random', methods=['POST'])
def chaos_inject_random():
    if not request.json or 'host' not in request.json:
        abort(400)
    dto = {
        'host': request.json['host'],
    }
    return jsonify(FaultInjector.chaos_inject_random(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/stop-specific-inject', methods=['POST'])
def stop_specific_inject():
    if not request.json or 'tag' not in request.json:
        abort(400)
    dto = {
        'tag': request.json['tag'],
    }
    return jsonify(FaultInjector.stop_chaos_inject(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade/view-inject-info', methods=['GET'])
def view_inject_info():
    return jsonify(FaultInjector.view_chaos_inject())