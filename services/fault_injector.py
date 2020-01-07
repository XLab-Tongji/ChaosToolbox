# -*- coding: utf-8 -*

import sys
import random
import json
import pika
import requests

from services.k8s_observer import K8sObserver
from utils.ansible_runner import Runner
from requests.exceptions import Timeout
from utils.log_record import Logger
from services.message_queue import RabbitMq

from config import DefaultCmd

username = 'guest'
pwd = 'guest'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='10.60.38.173', credentials=user_pwd
))
channel = connection.channel()
channel.queue_declare(queue='blade_mq')

sys.path.append('../')

target_url = "http://192.168.199.236:8080/reasoner/message"

Hosts = [
    "192.168.199.42",
    "192.168.199.43",
    "192.168.199.44",
    "192.168.199.45"
]

Spare_hosts = {
    "192.168.199.42": "192.168.199.32",
    "192.168.199.43": "192.168.199.33",
    "192.168.199.44": "192.168.199.34",
    "192.168.199.45": "192.168.199.35"
}

# 此部分已经移入配置文件
# Default_cmd = {
#     "cpu": "./blade create cpu fullload",
#     "network": "./blade create network delay --interface enp3s0 --time 1000",
#     "disk": "./blade create disk burn --read",
#     "mem": "./blade create mem load --mem-percent 80",
#     "k8s": "./blade create k8s delete --namespace sock-shop --pod"
# }


Cmd = {
    "cpu": "./blade create cpu fullload",
    "network": "./blade create network delay --interface enp3s0 ",
    "disk": "./blade create disk burn --",
    "mem": "./blade create mem load --mem-percent ",
    "k8s": "./blade create k8s delete --namespace sock-shop --pod ",
}
inject_info = []
has_injected = []
Default_cmd = {}



class FaultInjector(object):

    def __init__(self):
        pass

    @staticmethod
    def chaos_inject_cpu(dto):
        find = 0
        timeout = ''
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        if dto['timeout'] == 'default':
            timeout = ' --timeout 300'
        elif dto['timeout'] != 'no':
            timeout = ' --timeout ' + dto['timeout']
        target_inject = Cmd['cpu']
        for i in range(0, len(has_injected)):
            if has_injected[i]['host'] == target_host and has_injected[i]['inject_type'] == 'cpu':
                find = 1
        if find == 0:
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject + timeout)
            result = r.get_adhoc_result()
            return handle_inject_result('cpu', target_host, target_inject + timeout, result,
                                        sys._getframe().f_code.co_name, dto['open'])
        else:
            Logger.log("error",
                       "HOST HAS BEEN INJECTED - Method : " + sys._getframe().f_code.co_name + "() - - " + target_host)
            return "The host's cpu has been injected"

    @staticmethod
    def chaos_inject_mem(dto):
        find = 0
        timeout = ''
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        if dto['percent'] == 'default':
            target_inject = Default_cmd['mem']
        else:
            target_inject = Cmd['mem'] + dto['percent']
        if dto['timeout'] == 'default':
            timeout = ' --timeout 300'
        elif dto['timeout'] != 'no':
            timeout = ' --timeout ' + dto['timeout']
        for i in range(0, len(has_injected)):
            if has_injected[i]['host'] == target_host and has_injected[i]['inject_type'] == 'mem':
                find = 1
        if find == 0:
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject + timeout
            )
            result = r.get_adhoc_result()
            return handle_inject_result('mem', target_host, target_inject + timeout, result,
                                        sys._getframe().f_code.co_name, dto['open'])
        else:
            Logger.log("error",
                       "HOST HAS BEEN INJECTED - Method : " + sys._getframe().f_code.co_name + "() - - " + target_host)
            return "The host's mem has been injected"

    @staticmethod
    def chaos_inject_disk(dto):
        find = 0
        timeout = ''
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        if dto['type'] == 'default':
            target_inject = Default_cmd['disk']
        else:
            target_inject = Cmd['disk'] + dto['type']
        if dto['timeout'] == 'default':
            timeout = ' --timeout 300'
        elif dto['timeout'] != 'no':
            timeout = ' --timeout ' + dto['timeout']
        for i in range(0, len(has_injected)):
            if has_injected[i]['host'] == target_host and has_injected[i]['inject_type'] == 'disk':
                find = 1
        if find == 0:
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject + timeout
            )
            result = r.get_adhoc_result()
            return handle_inject_result('disk', target_host, target_inject + timeout, result,
                                        sys._getframe().f_code.co_name, dto['open'])
        else:
            Logger.log("error",
                       "HOST HAS BEEN INJECTED - Method : " + sys._getframe().f_code.co_name + "() - - " + target_host)
            return "The host's disk has been injected"

    @staticmethod
    def chaos_inject_network(dto):
        find = 0
        time = '3000'
        timeout = '600'
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        if dto['time'] != 'default':
            time = dto['time']
        if dto['timeout'] != 'default':
            timeout = dto['timeout']
        target_inject = Cmd['network'] + '--time ' + time + ' --timeout ' + timeout
        for i in range(0, len(has_injected)):
            if has_injected[i]['host'] == target_host and has_injected[i]['inject_type'] == 'network':
                find = 1
        if find == 0:
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject
            )
            result = r.get_adhoc_result()
            return handle_inject_result('network', target_host, target_inject + timeout, result,
                                        sys._getframe().f_code.co_name, dto['open'])
        else:
            return "The host's network has been injected"

    @staticmethod
    def chaos_inject_pod_single(dto):
        find = 0
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        target_inject = Cmd['k8s'] + dto['pod']
        for i in range(0, len(has_injected)):
            if has_injected[i]['host'] == target_host and has_injected[i]['inject_type'] == target_inject:
                find = 1
        if find == 0:
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject
            )
            result = r.get_adhoc_result()
            print(result)
            return handle_inject_result('k8s', target_host, target_inject, result,
                                        sys._getframe().f_code.co_name, dto['open'])
        else:
            return 'The pod has been injected'

    @staticmethod
    def chaos_inject_random(dto):
        global Default_cmd
        Default_cmd = DefaultCmd.get_default_cmd()
        find = 0
        timeout = ''
        pod_inject = ''
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        j = random.randint(0, len(Default_cmd) - 1)
        inject_type = Default_cmd.keys()[j]
        if inject_type == "k8s":
            pod_list = K8sObserver.get_pod_name_list("sock-shop")
            k = random.randint(0, len(pod_list) - 1)
            pod_inject = pod_list[k]
            target_inject = Default_cmd[Default_cmd.keys()[j]] + " " + pod_inject
        else:
            target_inject = Default_cmd[Default_cmd.keys()[j]]
        if dto['timeout'] == 'default':
            timeout = ' --timeout 300'
        elif dto['timeout'] != 'no':
            timeout = ' --timeout ' + dto['timeout']
        for i in range(0, len(has_injected)):
            if has_injected[i]['host'] == target_host and has_injected[i]['inject_type'] == target_inject:
                find = 1
        if find == 0:
            if inject_type != "k8s":
                target_inject = target_inject + timeout
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject
            )
            result = r.get_adhoc_result()
            return handle_inject_result(inject_type, target_host, target_inject, result,
                                        sys._getframe().f_code.co_name, dto['open'])
        else:
            Logger.log("error",
                       "HOST HAS BEEN INJECTED - Method : " + sys._getframe().f_code.co_name + "() - - " + str(dto))
            return "The host has been injected by the inject"

    @staticmethod
    def view_chaos_inject():
        return inject_info

    @staticmethod
    def view_inject_on_host_by_status(dto):
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + dto['host'] + ' does not exist.'
        target_inject = "./blade status --type create"
        status_type = str(dto['status']).capitalize()
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        inject_list = []
        if len(result['success']) > 0:
            transform_ip = result['success'].keys()[0]
            info = \
                json.loads(result['success'][transform_ip]['stdout'].encode('unicode-escape').decode('string_escape'))[
                    'result']
            for i in info:
                if i['Status'] == status_type:
                    inject_list.append(i)
            try:
                requests.post(url=target_url, params={'content': str(inject_list)}, verify=False, timeout=2)
            except Timeout:
                pass
            finally:
                Logger.log("info", "SUCCESS - Method : " + sys._getframe().f_code.co_name + "() - - " + str(dto))
                return inject_list
        else:
            if len(result["unreachable"]) > 0:
                transform_ip = result["unreachable"].keys()[0]
                message = result["unreachable"][transform_ip]["msg"]
                flag = "UNREACHABLE"
            else:
                transform_ip = result["failed"].keys()[0]
                message = result["failed"][transform_ip]["msg"]
                flag = "FAILED"
            view_info = {
                "ip": target_host,
                "status type": status_type,
                "cmd": target_inject,
                "message": message
            }
            Logger.log("error", flag + " - Method : " + sys._getframe().f_code.co_name + "() - - " + str(view_info))
        return inject_list

    @staticmethod
    def stop_specific_chaos_inject(dto):
        stop_id = dto['tag']
        target_host = ''
        find = 0
        key = 0
        for i in range(0, len(inject_info)):
            if inject_info[i]['cmd_id'] == stop_id:
                target_host = inject_info[i]['ip']
                find = 1
                key = i
        for i in range(0, len(has_injected)):
            if target_host == has_injected[i]['host'] and stop_id == has_injected[i]['tag']:
                has_injected.pop(i)
                break
        if find == 1:
            r = Runner()
            r.run_ad_hoc(
                hosts=Spare_hosts[inject_info[key]['ip']],
                module='shell',
                args='./blade destroy ' + stop_id
            )
            result = r.get_adhoc_result()
            if len(result["success"]) > 0:
                transform_ip = result["success"].keys()[0]
                the_stop_info = {
                    "position": inject_info[key]["position"],
                    "ip": Spare_hosts[inject_info[key]["ip"]],
                    "start_time": result["success"][transform_ip]["start"],
                    "cmd": result["success"][transform_ip]["cmd"],
                }
                inject_info.pop(key)
                Logger.log('info',
                           'SUCCESS - Method : ' + sys._getframe().f_code.co_name + "() - - " + str(the_stop_info))
                if dto['open'] == 'true':
                    RabbitMq.connect(the_stop_info)
                return result
            else:
                if len(result["unreachable"]) > 0:
                    transform_ip = result["unreachable"].keys()[0]
                    message = result["unreachable"][transform_ip]["msg"]
                    flag = "UNREACHABLE"
                else:
                    transform_ip = result["failed"].keys()[0]
                    message = result["failed"][transform_ip]["msg"]
                    flag = "FAILED"
                the_stop_info = {
                    "position": inject_info[key]["position"],
                    "ip": Spare_hosts[inject_info[key]["ip"]],
                    "cmd": "./blade destroy " + stop_id,
                    "message": message
                }
                Logger.log("error",
                           flag + " - Method : " + sys._getframe().f_code.co_name + "() - - " + str(the_stop_info))
                return result
        else:
            the_stop_info = {
                "cmd": "./blade destroy " + stop_id,
            }
            Logger.log('error',
                       'UID NOT FOUND -  Method : ' + sys._getframe().f_code.co_name + "() - - " + str(the_stop_info))
            return 'Inject not found'

    @staticmethod
    def stop_all_on_specific_node(dto):
        (target_host, is_exist) = get_target_host(dto)
        if not is_exist:
            return 'Host: ' + target_host + ' does not exist.'
        target_inject = './blade status --type create'
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        uid_list = []
        result_list = []
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            info = json.loads(result["success"][transform_ip]["stdout"]
                              .encode('unicode-escape')
                              .decode('string_escape'))["result"]
            for i in info:
                if i["Status"] == "Success":
                    uid_list.append(i["Uid"])
            if len(uid_list) == 0:
                Logger.log('info',
                           'NO CHAOS INJECT - Method : ' + sys._getframe().f_code.co_name + "() - - " + str(dto))
                return 'There is no injected attack on this host' + target_host
        for item in uid_list:
            cmd = './blade destroy ' + item
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=cmd
            )
            result = r.get_adhoc_result()
            # if len(result["success"]) > 0:
            #     for i in range(0, len(inject_info)):
            #         if inject_info[i]['cmd_id'] == item:
            #             if target_host == inject_info[i]['ip']:
            #                 inject_info.pop(i)
            #     for i in range(0, len(has_injected)):
            #         if target_host == has_injected[i]['host'] and item == has_injected[i]['tag']:
            #             has_injected.pop(i)
            #             break
            result_list.append(
                handle_inject_result("destroy", target_host, cmd, result, sys._getframe().f_code.co_name, dto['open']))
        return result_list

    @staticmethod
    def stop_all_chaos_inject_on_all_nodes(mq_control):
        uid_list = []
        result_list = []
        for target_host in Hosts:
            dto = {
                'host': target_host,
            }
            target_inject = './blade status --type create'
            r = Runner()
            r.run_ad_hoc(
                hosts=target_host,
                module='shell',
                args=target_inject
            )
            result = r.get_adhoc_result()
            if len(result["success"]) > 0:
                transform_ip = result["success"].keys()[0]
                info = json.loads(result["success"][transform_ip]["stdout"]
                                  .encode('unicode-escape')
                                  .decode('string_escape'))["result"]
                for i in info:
                    if i["Status"] == "Success":
                        uid_list.append(i["Uid"])
                if len(uid_list) == 0:
                    Logger.log('info',
                               'NO CHAOS INJECT - Method : ' + sys._getframe().f_code.co_name + "() - - " + str(dto))
            for item in uid_list:
                cmd = './blade destroy ' + item
                r = Runner()
                r.run_ad_hoc(
                    hosts=target_host,
                    module='shell',
                    args=cmd
                )
                result = r.get_adhoc_result()
                if len(result["success"]) > 0:
                    for i in range(0, len(inject_info)):
                        if inject_info[i]['cmd_id'] == item:
                            target_host = inject_info[i]['ip']
                            inject_info.pop(i)
                    for i in range(0, len(has_injected)):
                        if target_host == has_injected[i]['host'] and item == has_injected[i]['tag']:
                            has_injected.pop(i)
                            break
                result_list.append(
                    handle_inject_result("destroy", target_host, cmd, result, sys._getframe().f_code.co_name,
                                         mq_control['open']))
        return result_list

    @staticmethod
    def delete_all_pods_for_service(dto):
        """
        停止所有的某类容器[根据关键字删]
        :param service: 容器名中的关键字
        :return: 结果
        """
        service = dto["service"]
        result_list = []
        target_host = "10.60.38.181"
        name_list = K8sObserver.get_pod_name_list('sock-shop')
        for pod_name in name_list:
            if service in pod_name and (service + "-db") not in pod_name and (service + "-external") not in pod_name:
                target_inject = Cmd['k8s'] + pod_name
                r = Runner()
                r.run_ad_hoc(
                    hosts=target_host,
                    module='shell',
                    args=target_inject
                )
                result = r.get_adhoc_result()
                result_list.append(
                    handle_inject_result('k8s', target_host, target_inject, result,
                                         sys._getframe().f_code.co_name, dto['open']))
        return result_list

    @staticmethod
    def test_config():
        global Default_cmd
        Default_cmd = DefaultCmd.get_default_cmd()
        return Default_cmd


def handle_inject_result(inject_type, target_host, target_inject, result, method_name, mq_control):
    """
    处理返回结果
    :param inject_type: 注入类型
    :param target_host: 目标主机地址
    :param target_inject: 注入指令
    :param result: 注入结果
    :return: 注入结果
    :param method_name: 调用者的方法名
    """
    if len(result["success"]) > 0:
        transform_ip = result["success"].keys()[0]
        stdout = result["success"][transform_ip]["stdout"]
        result_ = stdout.split(',', 3)[2]
        tag_result = result_.split(':', 2)[1].replace('"', '').replace('}', '')
        the_has_injected = {
            "host": target_host.encode('unicode_escape').decode('string_escape'),
            "inject_type": inject_type,
            "tag": tag_result.encode('unicode_escape').decode('string_escape')
        }
        if inject_type != "destroy":
            has_injected.append(the_has_injected)
        the_inject_info = {
            "position": inject_type,
            "ip": target_host,
            "start_time": result["success"][transform_ip]["start"],
            "cmd": result["success"][transform_ip]["cmd"],
            "cmd_id": json.loads(
                result["success"][transform_ip]["stdout"].encode('unicode-escape').decode('string_escape'))[
                "result"].encode('unicode-escape').decode('string_escape')
        }
        if inject_type != "destroy":
            inject_info.append(the_inject_info)
        Logger.log('info', 'SUCCESS - Method : ' + method_name + "() - - " + str(the_inject_info))
        if mq_control == 'true':
            RabbitMq.connect(the_inject_info)
        return result
    else:
        if len(result["unreachable"]) > 0:
            transform_ip = result["unreachable"].keys()[0]
            message = result["unreachable"][transform_ip]["msg"]
            flag = "UNREACHABLE"
        else:
            transform_ip = result["failed"].keys()[0]
            message = result["failed"][transform_ip]["msg"]
            flag = "FAILED"
        the_inject_info = {
            "ip": target_host,
            "position": inject_type,
            "cmd": target_inject,
            "message": message
        }
        Logger.log("error", flag + " - Method : " + method_name + "() - - " + str(the_inject_info))
    return result


def get_target_host(dto):
    """
    获取目标主机地址
    :param dto: 注入参数
    :return: (目标主机, 存在与否) 若不存在, 返回值中的目标主机为提示语句
    """
    target_host = dto["host"]
    if target_host == "random":
        i = random.randint(0, len(Hosts) - 1)
        target_host = Hosts[i]
        return target_host, True
    if target_host not in Hosts:
        info = {
            "message": "Host: " + target_host + " does not exist.",
            "command info": dto
        }
        Logger.log("error", "HOST NOT EXIST - Method : " + sys._getframe().f_code.co_name + "() - - " + str(info))
        return target_host, False
    else:
        return target_host, True
