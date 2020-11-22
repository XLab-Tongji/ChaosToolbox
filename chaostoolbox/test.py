#import ansible_runner
from services.k8s_observer import K8sObserver
from flask import jsonify
import json

if __name__ == '__main__':
    res_json_str = K8sObserver.get_pod_name_list("sock-shop")
    print(res_json_str)
    #print(jsonify(res_json_str))