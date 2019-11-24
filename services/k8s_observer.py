# -*- coding: utf-8 -*

import sys
import os
import requests
import json
sys.path.append('../')
from utils.ansible_runner import Runner
from view_model.k8s_repository import K8sRepository


class K8sObserver(object):
    def __init__(self):
        pass

    @staticmethod
    def fetch_playbook_path(name):
        APP_ROOT = os.getcwd()
        return os.path.join(APP_ROOT, 'static', 'playbook', name)

    @staticmethod
    def get_namespace():
        r = Runner()
        r.run_playbook(
            playbooks=[K8sObserver.fetch_playbook_path('get_namespace.yaml')],
        )
        result = r.get_playbook_result()
        return K8sRepository.create_k8s_namespace_view_model(result)

    @staticmethod
    def get_node():
        r = Runner()
        r.run_playbook(
            playbooks=[K8sObserver.fetch_playbook_path('get_node.yaml')],
        )
        result = r.get_playbook_result()
        return K8sRepository.create_k8s_node_view_model(result)

    @staticmethod
    def get_svc(namespace):
        r = Runner()
        r.run_playbook(
            playbooks=[K8sObserver.fetch_playbook_path('get_svc.yaml')],
            extra_vars={'namespace': namespace}
        )
        result = r.get_playbook_result()
        return K8sRepository.create_k8s_svc_view_model(result)

    @staticmethod
    def get_deployment(namespace):
        r = Runner()
        r.run_playbook(
            playbooks=[K8sObserver.fetch_playbook_path('get_deployment.yaml')],
            extra_vars={'namespace': namespace}
        )
        result = r.get_playbook_result()
        return K8sRepository.create_k8s_deployment_view_model(result)

    @staticmethod
    def get_pods(namespace):
        r = Runner()
        r.run_playbook(
            playbooks=[K8sObserver.fetch_playbook_path('get_pod.yaml')],
            extra_vars={'namespace': namespace}
        )
        result = r.get_playbook_result()
        return K8sRepository.create_k8s_pods_view_model(result)

    @staticmethod
    def get_information_from_topology():
        url = "http://10.60.38.181:31009/api/topology?snapshot=hide&storage=hide&pseudo=hide&namespace="
        src_data = requests.get(url)
        json_data = json.loads(src_data.text)
        return json_data


    @staticmethod
    def batch_deliver_ssh():
        r = Runner()
        r.run_playbook(
            playbooks=[K8sObserver.fetch_playbook_path('batch_deliver_ssh.yaml')],
        )
        result=r.get_playbook_result()
        return result

    @staticmethod
    def get_pod_name_list(namespace):
        """
        获取某namespace下所有的pods名称

        注意: 该函数只供fault_injector.py调用
        :param namespace
        :return: pods name list
        """
        r = Runner()
        r.run_ad_hoc(
            hosts="10.60.38.181",
            module='shell',
            args="kubectl get pods -n " + namespace
        )
        result = r.get_adhoc_result()
        name_list = []
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            stdout_lines = result["success"][transform_ip]["stdout_lines"]
            for line in stdout_lines[1:]:
                line = line.split()
                name = line[0]
                name_list.append(name)
        return name_list


