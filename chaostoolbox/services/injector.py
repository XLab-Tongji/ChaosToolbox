import sys
import json
import random


sys.path.append('../')
from ansible_runner import MyAnsible
from services.k8s_observer import K8sObserver
from config.command import Command



class Injector:
    def __init__(self):
        pass
    
    @staticmethod
    def inject_random(dto):
        
        
        host = dto['host']

        name_list = K8sObserver.get_names(dto)
        k = random.randint(0,len(name_list) - 1)
        target = name_list[k]

        if dto.get('cpu_percent') == None: 
            #Inject Pod
            namespace = dto['namespace']
            args = Command.get_command('pod_injection', 'pod_delete') + "--names " +  target + " --namespace " + namespace + Command.get_command('config_info', 'kube_config')
        else:
            #Inject Node
            cpu_percent = dto['cpu_percent']
            args = Command.get_command('node_injection', "cpu_load") + "--cpu-percent " + cpu_percent + " --names " + target + Command.get_command('config_info', 'kube_config')

        r = MyAnsible()
        r.run(
            hosts = host,
            module = 'shell',
            args = args
        )
        r_result_dict = r.get_result()
        print(r_result_dict)
        r_success_dict = r_result_dict["success"]

        if len(r_success_dict) > 0:
            transform_ip = list(r_success_dict.keys())[0]
            res_info = r_success_dict[transform_ip]["stdout_lines"]
            return res_info
        else:
            return None



