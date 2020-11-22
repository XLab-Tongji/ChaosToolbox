import sys
import json
import random


sys.path.append('../')
from ansible_runner import MyAnsible
from services.k8s_observer import K8sObserver



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
            args = "blade create k8s pod-pod delete --names " +  target + " --namespace " + namespace + " --kubeconfig ~/.kube/config" 
        else:
            #Inject Node
            cpu_percent = dto['cpu_percent']
            args = "blade create k8s node-cpu load " + "--cpu-percent " + cpu_percent + " --names " + target + " --kubeconfig ~/.kube/config" 

        

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



