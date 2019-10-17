# -*- coding: utf-8 -*

import sys
import random
import json
import requests
from utils.ansible_runner import Runner
from requests.exceptions import Timeout

sys.path.append('../')

target_url = "http://192.168.199.236:8080/reasoner/message"

Hosts = [
    "192.168.199.41",
    "192.168.199.42",
    "192.168.199.43",
    "192.168.199.44",
    "192.168.199.45"
]

Spare_hosts = {
    "192.168.199.41": "192.168.199.31",
    "192.168.199.42": "192.168.199.32",
    "192.168.199.43": "192.168.199.33",
    "192.168.199.44": "192.168.199.34",
    "192.168.199.45": "192.168.199.35"
}

Default_cmd = {
    "cpu": "./blade create cpu fullload",
    "network": "./blade create network delay --interface enp2s0 --time 1000 --timeout 600",
    "disk": "./blade create disk burn --read",
    "mem": "./blade create mem load --mem-percent 80"
}

Cmd = {
    "cpu": "./blade create cpu fullload",
    "network": "./blade create network delay --interface enp2s0 ",
    "disk": "./blade create disk burn --",
    "mem": "./blade create mem load --mem-percent "
}

inject_info = []


class FaultInjector(object):
    def __init__(self):
        pass

    @staticmethod
    def chaos_inject_cpu(dto):
        target_inject = ''
        target_host = ''
        if dto['host'] == 'random':
            i = random.randint(0, len(Hosts) - 1)
            target_host = Hosts[i]
        else:
            target_host = dto['host']
        target_inject = Cmd["cpu"]
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            the_inject_info = {
                "position": "cpu",
                "ip": target_host,
                "start_time": result["success"][transform_ip]["start"],
                "cmd": result["success"][transform_ip]["cmd"],
                "cmd_id": json.loads(
                    result["success"][transform_ip]["stdout"].encode('unicode-escape').decode('string_escape'))[
                    "result"].encode('unicode-escape').decode('string_escape')
            }
            inject_info.append(the_inject_info)
            try:
                requests.post(url=target_url, params={"content": str(the_inject_info)}, verify=False, timeout=2)
            except Timeout:
                pass
            finally:
                return result
        return result

    @staticmethod
    def chaos_inject_mem(dto):
        target_inject = ''
        target_host = ''
        if dto['host'] == 'random':
            i = random.randint(0, len(Hosts) - 1)
            target_host = Hosts[i]
        else:
            target_host = dto['host']
        if dto['percent'] == 'default':
            target_inject = Default_cmd["mem"]
        else:
            target_inject = Cmd["mem"] + dto['percent']
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            the_inject_info = {
                "position": "mem",
                "ip": target_host,
                "start_time": result["success"][transform_ip]["start"],
                "cmd": result["success"][transform_ip]["cmd"],
                "cmd_id": json.loads(
                    result["success"][transform_ip]["stdout"].encode('unicode-escape').decode('string_escape'))[
                    "result"].encode('unicode-escape').decode('string_escape')
            }
            inject_info.append(the_inject_info)
            try:
                requests.post(url=target_url, params={"content": str(the_inject_info)}, verify=False, timeout=2)
            except Timeout:
                pass
            finally:
                return result
        return result

    @staticmethod
    def chaos_inject_disk(dto):
        target_inject = ''
        target_host = ''
        if dto['host'] == 'random':
            i = random.randint(0, len(Hosts) - 1)
            target_host = Hosts[i]
        else:
            target_host = dto['host']
        if dto['type'] == 'default':
            target_inject = Default_cmd["disk"]
        else:
            target_inject = Cmd["disk"] + dto['type']
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            the_inject_info = {
                "position": "disk",
                "ip": target_host,
                "start_time": result["success"][transform_ip]["start"],
                "cmd": result["success"][transform_ip]["cmd"],
                "cmd_id": json.loads(
                    result["success"][transform_ip]["stdout"].encode('unicode-escape').decode('string_escape'))[
                    "result"].encode('unicode-escape').decode('string_escape')
            }
            inject_info.append(the_inject_info)
            try:
                requests.post(url=target_url, params={"content": str(the_inject_info)}, verify=False, timeout=2)
            except Timeout:
                pass
            finally:
                return result
        return result

    @staticmethod
    def chaos_inject_network(dto):
        target_inject = ''
        target_host = ''
        time = '3000'
        timeout = '600'
        if dto['host'] == 'random':
            i = random.randint(0, len(Hosts) - 1)
            target_host = Hosts[i]
        else:
            target_host = dto['host']
        if dto['time'] != 'default':
            time = dto['time']
        if dto['timeout'] != 'default':
            timeout = dto['timeout']
        target_inject = Cmd['network'] + '--time ' + time + ' --timeout ' + timeout
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            the_inject_info = {
                "position": "network",
                "ip": target_host,
                "start_time": result["success"][transform_ip]["start"],
                "cmd": result["success"][transform_ip]["cmd"],
                "cmd_id": json.loads(
                    result["success"][transform_ip]["stdout"].encode('unicode-escape').decode('string_escape'))[
                    "result"].encode('unicode-escape').decode('string_escape')
            }
            inject_info.append(the_inject_info)
            try:
                requests.post(url=target_url, params={"content": str(the_inject_info)}, verify=False, timeout=2)
            except Timeout:
                pass
            finally:
                return result
        return result

    @staticmethod
    def chaos_inject_random(dto):
        target_inject = ''
        target_host = ''
        if dto['host'] == 'random':
            i = random.randint(0, len(Hosts)-1)
            target_host = Hosts[i]
        else:
            target_host = dto['host']
        j = random.randint(0, len(Cmd) - 1)
        target_inject = Default_cmd[Default_cmd.keys()[j]]
        r = Runner()
        r.run_ad_hoc(
            hosts=target_host,
            module='shell',
            args=target_inject
        )
        result = r.get_adhoc_result()
        if len(result["success"]) > 0:
            transform_ip = result["success"].keys()[0]
            the_inject_info = {
                "position": Default_cmd.keys()[j],
                "ip": target_host,
                "start_time": result["success"][transform_ip]["start"],
                "cmd": result["success"][transform_ip]["cmd"],
                "cmd_id": json.loads(result["success"][transform_ip]["stdout"].encode('unicode-escape').decode('string_escape'))["result"].encode('unicode-escape').decode('string_escape')
            }
            inject_info.append(the_inject_info)
            try:
                requests.post(url=target_url, params={"content": str(the_inject_info)}, verify=False, timeout=2)
            except Timeout:
                pass
            finally:
                return result
        return result

    @staticmethod
    def view_chaos_inject():
        return inject_info

    @staticmethod
    def stop_chaos_inject(dto):
        stop_id = dto['tag']
        find = 0
        key = 0
        for i in range(0, len(inject_info)):
            if inject_info[i]["cmd_id"] == stop_id:
                find = 1
                key = i
        if find == 1:
            r = Runner()
            r.run_ad_hoc(
                hosts=Spare_hosts[inject_info[key]["ip"]],
                module='shell',
                args="./blade destroy " + stop_id
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
                try:
                    requests.post(url=target_url, params={"content": str(the_stop_info)}, verify=False, timeout=2)
                except Timeout:
                    pass
                finally:
                    inject_info.pop(key)
                    return result
            else:
                inject_info.pop(key)
                return result
        else:
            return 'Inject not found'

