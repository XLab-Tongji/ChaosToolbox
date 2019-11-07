from flask import Blueprint, jsonify
from flask import request
from flask import abort
from services.fault_injector import FaultInjector
from utils.log_record import Logger

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


@chaosblade.route('/tool/api/v1.0/chaosblade/stop-all-inject', methods=['POST'])
def stop_all_inject():
    return jsonify(FaultInjector.stop_all_chaos_inject())


@chaosblade.route('/tool/api/v1.0/chaosblade/view-inject-info', methods=['GET'])
def view_inject_info():
    return jsonify(FaultInjector.view_chaos_inject())


@chaosblade.route('/tool/api/v1.0/chaosblade/view-all-create-error-inject-info', methods=['GET'])
def view_all_create_error_inject_info():
    return jsonify(FaultInjector.view_chaos_status_inject("Error"))


@chaosblade.route('/tool/api/v1.0/chaosblade/view-all-create-success-inject-info', methods=['GET'])
def view_all_create_success_inject_info():
    return jsonify(FaultInjector.view_chaos_status_inject("Success"))


@chaosblade.route('/tool/api/v1.0/chaosblade/view-all-create-destroy-inject-info', methods=['GET'])
def view_all_create_destroy_inject_info():
    return jsonify(FaultInjector.view_chaos_status_inject("Destroyed"))
