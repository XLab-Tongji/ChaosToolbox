
import sys
import json

sys.path.append('../')
from ansible_runner import MyAnsible


class K8sObserver:
    def __init__(self):
        pass
    
    @staticmethod
    def get_pod_name_list(dto):
        namespace = dto["namespace"]
        host = dto['host']
        
        r = MyAnsible()
        r.run(
            hosts=host,
            module="shell",
            args="kubectl get pods --namespace " + namespace
        )
        r_result_dict = r.get_result()
        
        r_success_dict = r_result_dict["success"]
        
        if len(r_success_dict) > 0:
            
            transform_ip = list(r_success_dict.keys())[0]
            stdout_lines = r_success_dict[transform_ip]["stdout_lines"]
            result_json_str = json.dumps(stdout_lines)
            #return stdout_lines
            return result_json_str
            #print(result_json_str)
        #result_json_str = json.dumps(result_dict)
        #print(result_json_str)
