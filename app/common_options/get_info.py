from flask import Blueprint, jsonify
from services.k8s_observer import K8sObserver

get_info = Blueprint('get_info', __name__)


@get_info.route('/tool/api/v1.0/get_namespace', methods=['GET'])
def get_namespace():
    return jsonify(K8sObserver.get_namespace())


@get_info.route('/tool/api/v1.0/get_node')
def get_node():
    return jsonify(K8sObserver.get_node())


@get_info.route('/tool/api/v1.0/get_svc/<namespace>', methods=['GET'])
def get_svc(namespace):
    return jsonify(K8sObserver.get_svc(namespace=namespace.encode('raw_unicode_escape')))


@get_info.route('/tool/api/v1.0/get_deployment/<namespace>', methods=['GET'])
def get_deployment(namespace):
    return jsonify(K8sObserver.get_deployment(namespace=namespace.encode('raw_unicode_escape')))


@get_info.route('/tool/api/v1.0/get_pods/<namespace>', methods=['GET'])
def get_pods(namespace):
    return jsonify(K8sObserver.get_pods(namespace=namespace.encode('raw_unicode_escape')))


@get_info.route('/tool/api/v1.0/get-information-from-topology', methods=['GET'])
def get_information_from_topology():
    return jsonify(K8sObserver.get_information_from_topology())
