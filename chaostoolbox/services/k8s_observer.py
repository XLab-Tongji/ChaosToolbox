import sys
import json

sys.path.append('../')
from ansible_runner import MyAnsible


class K8sObserver:
    def __init__(self):
        pass
    
    @staticmethod
    def get_info(dto):
        host = dto['host']

        if dto.get('namespace') == None:
            args = "kubectl get nodes"
        else:
            args = "kubectl get pods --namespace " + dto["namespace"]
        

        r = MyAnsible()
        r.run(
            hosts=host,
            module="shell",
            args=args
        )
        r_result_dict = r.get_result()
        r_success_dict = r_result_dict["success"]
        
        if len(r_success_dict) > 0:
            
            transform_ip = list(r_success_dict.keys())[0]
            res_info = r_success_dict[transform_ip]["stdout_lines"]

            return res_info

        else:
            return None

    @staticmethod
    def get_names(dto):
        res_name_list = []

        info_str = K8sObserver.get_info(dto)

        for line in info_str[1:]:
            line = line.split()
            name = line[0]
            res_name_list.append(name)

        return res_name_list
    





