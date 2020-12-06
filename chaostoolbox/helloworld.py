import sys
from services.k8s_observer import K8sObserver
from services.injector import Injector
from flask import Flask
from flask import request, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<host>/pod', methods = ['GET'])
def get_pods(host):

    namespace = request.args.get('namespace', default = 'sock-shop', type = str)
    name_only = request.args.get('name_only', default = 0, type = int)


    dto = {
        'host' : host,
        'namespace' : namespace
    }

    if name_only:
        return jsonify(K8sObserver.get_names(dto))

    return jsonify(K8sObserver.get_info(dto))


@app.route('/<host>/node', methods = ['GET'])
def get_nodes(host):

    name_only = request.args.get('name_only', default = 0, type = int)
    
    dto = {
        'host' : host
    }

    if name_only:
        return jsonify(K8sObserver.get_names(dto))

    return jsonify(K8sObserver.get_info(dto))


@app.route('/<host>/inject/node/random', methods = ['POST'])
def inject_random_node(host):

    dto = {
        'host' : host,
        'cpu_percent' : request.json['cpu_percent']
    }
    return jsonify(Injector.inject_random(dto))

@app.route('/<host>/inject/pod/random', methods = ['POST'])
def inject_random_pod(host):

    dto = {
        'host' : host,
        'namespace' : request.json['namespace']
    }
    return jsonify(Injector.inject_random(dto))








