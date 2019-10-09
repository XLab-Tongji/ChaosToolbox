from flask import Blueprint, jsonify
from flask import request
from flask import abort
from services.fault_injector import FaultInjector

chaosblade = Blueprint('chaosblade', __name__)


@chaosblade.route('/tool/api/v1.0/chaosblade-vm/inject', methods=['POST'])
def chaos_injectvm():
    if not request.json or 'type' not in request.json or 'host' not in request.json:
        abort(400)
    dto = {
        'type': request.json['type'],
        # 'inject_duration': request.json['duration']
        'host': request.json['host']
    }
    return jsonify(FaultInjector.chaos_inject_vm(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade-vm/stop-specific-inject', methods=['POST'])
def stop_specific_inject():
    if not request.json or 'tag' not in request.json:
        abort(400)
    dto = {
        'tag': request.json['tag'],
    }
    return jsonify(FaultInjector.stop_chaosinject_vm(dto))


@chaosblade.route('/tool/api/v1.0/chaosblade-vm/view-inject-info', methods=['GET'])
def view_inject_info():
    return jsonify(FaultInjector.view_chaos_inject_vm())