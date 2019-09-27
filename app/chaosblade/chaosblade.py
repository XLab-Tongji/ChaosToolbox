from flask import Blueprint, jsonify
from flask import request
from flask import abort
from services.fault_injector import FaultInjector

chaosblade = Blueprint('chaosblade', __name__)


@chaosblade.route('/tool/api/v1.0/chaosbladevm/inject', methods=['POST'])
def chaosinjectvm():
    if not request.json or not 'duration' in request.json:
        abort(400)
    dto = {
        # 'type': request.json['type'],
        'inject_duration': request.json['duration']
        # 'host': request.json['host']
    }
    # if dto['type'] == 'cpu':
    return jsonify(FaultInjector.chaosinjectvm(dto))
