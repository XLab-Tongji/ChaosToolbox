import sys
import json
import random


sys.path.append('../')
from ansible_runner import MyAnsible
from services.k8s_observer import K8sObserver
from config.command import Command


'''
This class injects the target host
'''
class Injector:
    def __init__(self):
        pass
    
    '''
    This function implements random injection
    dto : dict
    '''
    @staticmethod
    def inject_random(dto):
        
        
        host = dto['host']
        # Get name list according to given dto
        name_list = K8sObserver.get_names(dto)

        # Generate random injection target
        k = random.randint(0,len(name_list) - 1)
        target = name_list[k]

        if dto.get('cpu_percent') == None: 
            # Inject Pod
            namespace = dto['namespace']
            args = Command.get_command('pod_injection', 'pod_delete') + "--names " +  target + " --namespace " + namespace + Command.get_command('config_info', 'kube_config')
        else:
            # Inject Node
            cpu_percent = dto['cpu_percent']
            args = Command.get_command('node_injection', "cpu_load") + "--cpu-percent " + cpu_percent + " --names " + target + Command.get_command('config_info', 'kube_config')

        # Run command and get result
        r = MyAnsible()
        r.run(
            hosts = host,
            module = 'shell',
            args = args
        )
        r_result_dict = r.get_result()
        print(r_result_dict)
        r_success_dict = r_result_dict["success"]

        # Handle result
        if len(r_success_dict) > 0:
            transform_ip = list(r_success_dict.keys())[0]
            res_info = r_success_dict[transform_ip]["stdout_lines"]
            return res_info
        else:
            return None



