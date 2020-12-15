import sys
import logging
import datetime
import os
from services.k8s_observer import K8sObserver
from services.injector import Injector
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.SockConfig import Config
from utils.utils import Utils
from controller.prometheus.PerformanceDataPicker import PerformanceDataPicker
from controller.prometheus.PerformanceDataWriter import PerformanceDataWriter


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
def inject_random_node(host):

    dto = {
        'host' : host,
        'cpu_percent' : request.json.get('cpu_percent')
    }
    return jsonify(Injector.inject_random(dto))

@app.route('/<host>/inject/pod/random', methods = ['POST'])
def inject_random_pod(host):

    dto = {
        'host' : host,
        'namespace' : request.json.get('namespace')
    }
    return jsonify(Injector.inject_random(dto))

@app.route('/acquire-data', methods=['GET'])
def acquire_data():
    result = {}
    result["message"] = main()
    return jsonify(result)


def main():
    curr_time = datetime.datetime.now()
    START_STR = ""
    END_STR = ""
    if curr_time.hour < 10:
        START_STR = str(curr_time.date()) + " 0" + str(curr_time.hour - 1) + ":30:00"
        END_STR = str(curr_time.date()) + " 0" + str(curr_time.hour) + ":00:00"
    elif curr_time.hour == 10:
        START_STR = str(curr_time.date()) + " 0" + str(curr_time.hour - 1) + ":30:00"
        END_STR = str(curr_time.date()) + " " + str(curr_time.hour) + ":00:00"
    else:
        START_STR = str(curr_time.date()) + " " + str(curr_time.hour - 1) + ":30:00"
        END_STR = str(curr_time.date()) + " " + str(curr_time.hour) + ":00:00"

    RESOLUTION = Config.PROMETHEUS_RESOLUTION

    end_time = Utils.datetime_timestamp(END_STR)
    start_time = Utils.datetime_timestamp(START_STR)

    headers, csvsets = PerformanceDataPicker.query_multi_entity_metric_values(queryconfiglist=Config.QUERY_CONFIGS_HW,
                                                                              resolution=Config.PROMETHEUS_RESOLUTION,
                                                                              start_time=start_time,
                                                                              end_time=end_time)
    dirs = "/code/chaostoolbox/data/prometheus/" + curr_time.strftime("%Y-%m")
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    target_file = dirs + "/" + START_STR.replace("-", "").replace(":", "").replace(" ", "_") + "_SockShopPerformance.csv"
    PerformanceDataWriter.write2csv_merged(
        filename=target_file,
        metricsnameset=headers, datasets=csvsets)
    return "success"





