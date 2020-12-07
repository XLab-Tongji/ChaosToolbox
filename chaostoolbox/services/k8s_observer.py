import sys
import json

sys.path.append('../')
from ansible_runner import MyAnsible
from config.command import Command

'''
This class gets kubernetes information
'''
class K8sObserver:
    def __init__(self):
        pass
    
    '''
    This function get full information of nodes or pods
    dto : dict
    ret_val : list
    '''
    @staticmethod
    def get_info(dto):
        # Decodes dto and get commands
        (host, namespace) = (dto.get('host'), dto.get('namespace'))
        
        if namespace == None:
            args = Command.get_command('kubernetes_info', 'node_info')
        elif namespace == 'all':
            args = Command.get_command('kubernetes_info', 'pod_info') + " --all-namespaces"
        else:
            args = Command.get_command('kubernetes_info', 'pod_info') + " --namespace " + namespace
        
        # Run ansible
        r = MyAnsible()
        r.run(
            hosts=host,
            module="shell",
            args=args
        )
        r_result_dict = r.get_result()
        r_success_dict = r_result_dict["success"]
        
        # Handle return result
        if len(r_success_dict) > 0:
            
            transform_ip = list(r_success_dict.keys())[0]
            res_info = r_success_dict[transform_ip]["stdout_lines"]

            return res_info

        else:
            return "Injection failed"


    '''
    This function only return name of nodes or pods
    It gets all information firstly and then slice
    dto: dict
    ret_val : list
    '''
    @staticmethod
    def get_names(dto):
        # Initialize return value
        res_name_list = []

        # Get all information
        info_str = K8sObserver.get_info(dto)

        # Slice
        for line in info_str[1:]:
            line = line.split()
            name = line[0]
            res_name_list.append(name)

        return res_name_list
    





