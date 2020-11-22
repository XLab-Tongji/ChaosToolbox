import sys
from services.k8s_observer import K8sObserver
from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pods', methods = ['POST'])
def get_pods():
    #TODO: Input check
    """
    {
    "host":"Lab409_master",
    "namespace":"sock-shop"
    }
    """
    dto = {
        'host' : request.json['host'],
        'namespace' : request.json['namespace']
    }
    return K8sObserver.get_pod_name_list(dto)




