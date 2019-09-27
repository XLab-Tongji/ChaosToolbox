from flask import Blueprint, jsonify
from services.k8s_observer import K8sObserver

get_info = Blueprint('get_info', __name__)


@get_info.route('/tool/api/v1.0/get_namespace', methods=['GET'])
# @auth.login_required
def get_namespace():
    return jsonify(K8sObserver.get_namespace())


@get_info.route('/tool/api/v1.0/get_node')
def get_node():
    return jsonify(K8sObserver.get_node())


@get_info.route('/tool/api/v1.0/get_svc/<namespace>', methods=['GET'])
def get_svc(namespace):
    return jsonify(K8sObserver.get_svc(namespace=namespace.encode('raw_unicode_escape')))



