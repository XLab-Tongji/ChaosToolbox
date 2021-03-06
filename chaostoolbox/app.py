import sys
import logging
import datetime
import os
from services.k8s_observer import K8sObserver
from services.injector import Injector
from flask import Flask, request, jsonify
from flask_cors import CORS





app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<host>/pod', methods = ['GET'])
def get_pods(host):

    namespace = request.args.get('namespace', default = 'all', type = str)
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
def inject_node_random(host):

    dto = {
        'host' : host,
        'cpu-percent' : request.json.get('cpu-percent')
    }
    return jsonify(Injector.inject_random(dto))

@app.route('/<host>/inject/node/cpu', methods = ['POST'])
def inject_node_cpu(host):

    dto = {
        
        'host' : host,
        'names' : request.json.get('names'),
        'cpu-percent': request.json.get('cpu-percent') 
    }
    return jsonify(Injector.inject_node_cpu(dto))

@app.route('/<host>/inject/node/network/delay', methods = ['POST'])
def inject_node_network_delay(host):

    dto = {
        'host' : host,
        'names' : request.json.get('names'),
        'local-port' : request.json.get('local-port'),
        'time' : request.json.get('time'),
        'offset' : request.json.get('offset'),
        'interface' : ''
    }
    return jsonify(Injector.inject_node_network_delay(dto))

@app.route('/<host>/inject/node/network/loss', methods = ['POST'])
def inject_node_network_loss(host):

    dto = {
        'host' : host,
        'names' : request.json.get('names'),
        'percent' : request.json.get('percent'),
        'interface' : ''
    }
    return jsonify(Injector.inject_node_network_loss(dto))

@app.route('/<host>/inject/node/disk', methods = ['POST'])
def inject_node_disk(host):

    dto = {
        'host' : host,
        'names' : request.json.get('names'),
        'percent' : request.json.get('percent')
    }
    return jsonify(Injector.inject_node_disk(dto))

@app.route('/<host>/inject/node/process', methods = ['POST'])
def inject_node_process(host):

    dto = {
        'host' : host,
        'process' : request.json.get('process'),
        'percent' : request.json.get('names')
    }
    return jsonify(Injector.inject_node_process(dto))


@app.route('/<host>/inject/pod/random', methods = ['POST'])
def inject_pod_random(host):

    dto = {
        'host' : host,
        'namespace' : request.json.get('namespace')
    }
    return jsonify(Injector.inject_random(dto))

@app.route('/<host>/inject/pod/delete/label', methods = ['POST'])
def inject_pod_delete_by_label(host):

    pass

@app.route('/<host>/inject/pod/delete/name', methods = ['POST'])
def inject_pod_delete_by_name(host):
    dto = {
        'host' : host,
        'names' : request.json.get('names'),
        'namespace' : request.json.get('namespace'),
        'evict-count' : request.json.get('evict-count')
    }
    return jsonify(Injector.inject_pod_delete_by_name(dto))
    
@app.route('/<host>/inject/pod/network/delay', methods = ['POST'])
def inject_pod_network_delay(host):

    dto = {
        'host' : host,
        'names' : request.json.get('names'),
        'namespace' : request.json.get('sock-shop'),
        'local-port' : request.json.get('local-port'),
        'interface' : request.json.get('interface'),
        'time' : request.json.get('time'),
        'offset' : request.json.get('offset')
    }
    return jsonify(Injector.inject_pod_network_delay(dto))

@app.route('/<host>/inject/pod/network/loss', methods = ['POST'])
def inject_pod_network_loss(host):

    dto = {
        'host' : host,
        'names' : request.json.get('names'),
        'namespace' : request.json.get('sock-shop'),
        'local-port' : request.json.get('local-port'),
        'interface' : request.json.get('interface'),
        'percent' : request.json.get('percent')
    } 
    return jsonify(Injector.inject_pod_network_loss(dto))

@app.route('/<host>/inject/pod/network/dns', methods = ['POST'])
def inject_pod_network_dns(host):

    dto = {
        'host' : host,
        'namespace' : request.json.get('namespace'),
        'names' : request.json.get('names'),
        'domain' : request.json.get('domain'),
        'ip' : request.json.get('ip')
    }
    return jsonify(Injector.inject_pod_network_dns(dto))

@app.route('/<host>/destroy', methods = ['POST'])
def destroy_injection(host):
    dto = {
        'host' : host,
        'uid' : request.json.get('uid')
    }
    return jsonify(Injector.destroy_injection(dto))


@app.route('/<host>/destroy/all', methods = ['POST'])
def destroy_all(host):
    dto = {
        'host' : host
    }
    return jsonify(Injector.destroy_all(dto))

@app.route('/prometheus/log', methods=['GET'])
def get_prometheus_log():
    result = {}
    result["message"] = K8sObserver.get_prometheus_log()
    return jsonify(result)


@app.route('/weavescope/topology', methods=['GET'])
def get_weavescope_topology_info():
    result = K8sObserver.get_weavescope_topology_info()
    return jsonify(result)










