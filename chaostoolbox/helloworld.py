import sys
from services.k8s_observer import K8sObserver
from services.injector import Injector
from flask import Flask
from flask import request, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pod', methods = ['POST'])
def get_pods():
    dto = {
        'host' : request.json['host'],
        'namespace' : request.json['namespace']
    }
    return jsonify(K8sObserver.get_info(dto))

@app.route('/pod/name', methods = ['POST'])
def get_pod_names():
    dto = {
        'host' : request.json['host'],
        'namespace' : request.json['namespace']
    }
    return jsonify(K8sObserver.get_names(dto))

@app.route('/node', methods = ['POST'])
def get_nodes():
    dto = {
        'host' : request.json['host']
    }
    return jsonify(K8sObserver.get_info(dto))

@app.route('/node/name', methods = ['POST'])
def get_node_names():
    dto = {
        'host' : request.json['host']
    }
    return jsonify(K8sObserver.get_names(dto))

@app.route('/inject/node/random', methods = ['POST'])
def inject_random_node():
    dto = {
        'host' : request.json['host'],
        'cpu_percent' : request.json['cpu_percent']
    }
    return jsonify(Injector.inject_random(dto))

@app.route('/inject/pod/random', methods = ['POST'])
def inject_random_pod():
    dto = {
        'host' : request.json['host'],
        'namespace' : request.json['namespace']
    }
    return jsonify(Injector.inject_random(dto))








