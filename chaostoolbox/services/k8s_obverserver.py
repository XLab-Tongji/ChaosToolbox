# -*- coding: utf-8 -*

import sys
import os
import time

import requests
import json

from utils.log_record import Logger

sys.path.append('../')
from utils.ansible_runner import Runner
from view_model.k8s_repository import K8sRepository
import datetime

service_name = [
    "carts",
    "carts-db",
    "catalogue",
    "catalogue-db",
    "front-end",
    "front-end-external",
    "orders",
    "orders-db",
    "payment",
    "queue-master",
    "rabbitmq",
    "session-db",
    "shipping",
    "user",
    "user-db",
]


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
        result = r.get_playbook_result()
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
            args="/opt/kube/bin/kubectl get pods -n " + namespace
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

    @staticmethod
    def get_service_log(service, namespace):
        """
        获取某个namespace下, 指定service的全部日志
        :param service: service name
        :param namespace: namespace
        :return: success or failed
        """
        if service not in service_name:
            info = {
                "error": "The service does not exist. Please check the service name!",
            }
            Logger.log("error",
                       "SERVICE NOT EXIST - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
            return "The service" + service + " does not exist. Please check the service name!"
        r = Runner()
        r.run_ad_hoc(
            hosts="10.60.38.181",
            module='shell',
            args="/opt/kube/bin/kubectl get pods -n " + namespace
        )
        result = r.get_adhoc_result()
        name_list = []
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            stdout_lines = result["success"][transform_ip]["stdout_lines"]
            for line in stdout_lines[1:]:
                if service in line and (service + "-db") not in line and (service + "-external") not in line:
                    line = line.split()
                    name = line[0]
                    name_list.append(name)
                else:
                    continue
            print
            name_list
            if len(name_list) != 0:
                info = {
                    "success": "The  " + service + "service pod list was successfully obtained!",
                    "pod": name_list
                }
                Logger.log("info",
                           "SUCCESS - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
            else:
                info = {
                    "error": "The service" + service + " has no pod list!",
                }
                Logger.log("error",
                           "NO POD - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
                return "The service" + service + " has no pod list!"
        else:
            if len(result["unreachable"]) > 0:
                transform_ip = result["unreachable"].keys()[0]
                message = result["unreachable"][transform_ip]["msg"]
                flag = "UNREACHABLE"
            else:
                transform_ip = result["failed"].keys()[0]
                message = result["failed"][transform_ip]["msg"]
                flag = "FAILED"
            info = {
                "error": "Failed to get the pod list of service " + service,
                "message": message
            }
            Logger.log("error",
                       flag + " - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
            return "Failed to get the pod list of services " + service
        request_time = time.strftime('%Y-%m-%d/%H:%M:%S', time.localtime(time.time()))
        result = []
        for pod_name in name_list:
            result.append(get_pod_log(pod_name, namespace, request_time))
        return result

    @staticmethod
    def get_pods_status(namespace):
        r = Runner()
        r.run_ad_hoc(
            hosts="10.60.38.181",
            module='shell',
            args='/opt/kube/bin/kubectl get pods -n ' + namespace
        )
        result = r.get_adhoc_result()
        result_status = []
        if len(result['success']) > 0:
            host_name = result['success'].keys()[0]
            stdout_lines = result['success'][host_name]['stdout_lines']
            for index in range(1, len(stdout_lines)):
                stdout_line = stdout_lines[index].split()
                result_status.append({
                    'name': stdout_line[0],
                    'status': stdout_line[2],
                    'restarts': stdout_line[3],
                    'age': stdout_line[4],
                })

            return result_status


def get_pod_log(pod_name, namespace, request_time):
    """
    获取某个namespace下, 指定pod的日志, 并输出到指定的文件夹
    :param pod_name: pod name
    :param namespace: namespace
    :param request_time: 发出请求的时间
    :return: success or failed
    """
    dir_name = request_time
    command = '/opt/kube/bin/kubectl logs ' + pod_name + ' -n ' + namespace
    r = Runner()
    r.run_ad_hoc(
        hosts="10.60.38.181",
        module='shell',
        args=command
    )
    result = r.get_adhoc_result()
    if len(result["success"]) > 0:

        transform_ip = result["success"].keys()[0]
        stdout_lines = result["success"][transform_ip]["stdout_lines"]
        cwd = os.getcwd()
        dir_path = cwd + "/pod_log_dir/" + str(dir_name)
        is_exist = os.path.exists(dir_path)
        if not is_exist:
            os.makedirs(dir_path)
        log_path = dir_path + "/" + pod_name + ".txt"
        with open(log_path, 'a') as f:
            for line in stdout_lines:
                f.write(line)
                f.write('\n')
        info = {
            "pod name": pod_name,
            "command": command,
            "log path": log_path
        }
        Logger.log("info", "SUCCESS - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
    else:
        if len(result["unreachable"]) > 0:
            transform_ip = result["unreachable"].keys()[0]
            message = result["unreachable"][transform_ip]["msg"]
            flag = "UNREACHABLE"
        else:
            transform_ip = result["failed"].keys()[0]
            message = result["failed"][transform_ip]["msg"]
            flag = "FAILED"
        info = {
            "pod name": pod_name,
            "command": command,
            "message": message
        }
        Logger.log("error",
                   flag + " - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
    return info
