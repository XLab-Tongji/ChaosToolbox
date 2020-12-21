import sys
import json
import requests
import datetime
import os

sys.path.append('../')
from ansible_runner import MyAnsible
from config.command import Command
from utils.SockConfig import Config
from utils.utils import Utils
from controller.prometheus.PerformanceDataPicker import PerformanceDataPicker
from controller.prometheus.PerformanceDataWriter import PerformanceDataWriter

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
    
    @staticmethod
    def get_weavescope_topology_info():
        url = "http://10.60.38.174:31009/api/topology?snapshot=hide&storage=hide&pseudo=hide&namespace="
        src_data = requests.get(url)

        ret_json_data = json.loads(src_data.text)

        return ret_json_data 

    @staticmethod
    def get_prometheus_log():
        curr_time = datetime.datetime.now()
        START_STR = ""
        END_STR = ""
        if curr_time.hour < 10:
            START_STR = str(curr_time.date()) + " 0" + str(curr_time.hour - 1) + ":30:00"
            END_STR = str(curr_time.date()) + " 0" + str(curr_time.hour) + ":00:00"
        elif curr_time.hour == 10:
            START_STR = str(curr_time.date()) + " 0" + str(curr_time.hour - 1) + ":30:00"
            END_STR = str(curr_time.date()) + " " + str(curr_time.hour) + ":00:00"
        else:
            START_STR = str(curr_time.date()) + " " + str(curr_time.hour - 1) + ":30:00"
            END_STR = str(curr_time.date()) + " " + str(curr_time.hour) + ":00:00"

        RESOLUTION = Config.PROMETHEUS_RESOLUTION

        end_time = Utils.datetime_timestamp(END_STR)
        start_time = Utils.datetime_timestamp(START_STR)

        headers, csvsets = PerformanceDataPicker.query_multi_entity_metric_values(queryconfiglist=Config.QUERY_CONFIGS_HW,
                                                                                resolution=Config.PROMETHEUS_RESOLUTION,
                                                                                start_time=start_time,
                                                                                end_time=end_time)
        dirs = "/code/chaostoolbox/data/prometheus/" + curr_time.strftime("%Y-%m")
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        target_file = dirs + "/" + START_STR.replace("-", "").replace(":", "").replace(" ", "_") + "_SockShopPerformance.csv"
        PerformanceDataWriter.write2csv_merged(
            filename=target_file,
            metricsnameset=headers, datasets=csvsets)
        return "success"




