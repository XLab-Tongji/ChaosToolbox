# -*- coding: utf-8 -*

import sys
import random
import json
import ast
from utils.ansible_runner import Runner

sys.path.append('../')

Hosts = [
    "192.168.199.31",
    "192.168.199.32",
    "192.168.199.33",
    "192.168.199.34",
    "192.168.199.35"
]

HostsVM = [
    "192.168.199.21",
    "192.168.199.22",
    "192.168.199.23",
    "192.168.199.24",
    "192.168.199.25"
]

Cmd = {
    "cpu": "blade create cpu fullload",
    "network": "blade create network delay --interface ens160",
    "disk": "blade create disk fill --size 1000"
}

inject_info = []


class FaultInjector(object):
    def __init__(self):
        pass

    @staticmethod
    def inject_cpu(dto):
        r = Runner()
        r.run_ad_hoc(
            hosts=dto['host'],
            module='shell',
            args='stress -c 1 -t ' + dto['inject_duration'] + ' > /dev/null 2>&1'
        )
        result = r.get_adhoc_result()
        return result

    @staticmethod
    def inject_mem(dto):
        r = Runner()
        r.run_ad_hoc(
            hosts=dto['host'],
            module='shell',
            args='stress --vm 4 --vm-bytes 1G --vm-hang ' + dto['inject_duration'] + ' -t '
                 + dto['inject_duration'] + ' > /dev/null 2>&1'
        )
        result = r.get_adhoc_result()
        return result

    @staticmethod
    def inject_io(dto):
        r = Runner()
        r.run_ad_hoc(
            hosts=dto['host'],
            module='shell',
            args='stress -i 100 -t ' + dto['inject_duration'] + ' > /dev/null 2>&1'
        )
        result = r.get_adhoc_result()
        return result

    @staticmethod
    def chaosinject(dto):
        i=random.randint(0, 4)
        j=random.randint(0, 2)
        r = Runner()
        r.run_ad_hoc(
            hosts=Hosts[i],
            module='shell',
            args=Cmd[j]+" --timeout " + dto['inject_duration']
        )
        result = r.get_adhoc_result()
        return result

    @staticmethod
    def chaosinject1(dto):
        #i=random.randint(0, 4)
        #j=random.randint(0, 2)
        r = Runner()
        r.run_ad_hoc(
            hosts="192.168.199.31",
            module='shell',
            args="blade create disk fill --size 1000 --timeout " + dto['inject_duration']
        )
        result = r.get_adhoc_result()
        return result

    @staticmethod
    def chaos_inject_vm(dto):
        target_inject = ''
        target_host = ''
        if dto['host'] == 'random':
            i = random.randint(0, len(HostsVM)-1)
            target_host = HostsVM[i]
        else:
            target_host = dto['host']
        if dto['type'] == 'random':
            j = random.randint(0, len(Cmd)-1)
            target_inject = Cmd[Cmd.keys()[j]]
        else:
            target_inject = Cmd[dto['type']]
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
                "position": target_inject,
                "ip": target_host,
                "start_time": result["success"][transform_ip]["start"],
                "cmd": result["success"][transform_ip]["cmd"],
                "cmd_id": json.loads(result["success"][transform_ip]["stderr"].encode('unicode-escape').decode('string_escape'))["result"].encode('unicode-escape').decode('string_escape')
            }
            inject_info.append(the_inject_info)
        return result

    @staticmethod
    def view_chaos_inject_vm():
        return inject_info

    @staticmethod
    def stop_chaosinject_vm(dto):
        stop_id = dto['tag']
        find = 0
        key = 0
        for i in range(0, len(inject_info)):
            if inject_info[i]["cmd_id"] == stop_id:
                find = 1
                key = i
        a = inject_info[key]["ip"]
        if find == 1:
            r = Runner()
            r.run_ad_hoc(
                hosts=inject_info[key]["ip"],
                module='shell',
                args="blade destroy " + stop_id
            )
            inject_info.pop(key)
            result = r.get_adhoc_result()
            return result
        else:
            return 'Inject not found'

