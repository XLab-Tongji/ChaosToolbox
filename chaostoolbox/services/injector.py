import sys
import json
import random


sys.path.append('../')
from configs.command import Command
from ansible_runner import MyAnsible
from services.k8s_observer import K8sObserver
from services.runner import Runner
from services.handler import Handler
from utils.logger import Logger



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

        target = K8sObserver.get_random_name(dto)
        
        if dto.get('cpu-percent') == None: 
            # Inject Pod
            namespace = dto['namespace']
            args = Command.get_command('pod_injection', 'pod_delete') \
                + "--names " +  target \
                + " --namespace " + namespace \
                + Command.get_config()
        else:
            # Inject Node
            cpu_percent = dto['cpu-percent']
            args = Command.get_command('node_injection', 'cpu_load') \
                + "--cpu-percent " + cpu_percent \
                + " --names " + target \
                + Command.get_config()


        r_success_dict = Runner.run_adhoc(host, args)

        # Handle result
        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_node_cpu(dto):
        host= dto['host']

        args = Command.get_command('node_injection', 'cpu_load') \
            + Command.parser(dto) \
            + Command.get_config()
        #print(args)
        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_node_network_delay(dto):
        (host, names) = (dto['host'], dto['names'])

        args = Command.get_command('node_injection', 'network_delay') \
            + Command.parser(dto) \
            + Command.get_command('network_interface', 'node_' + names) \
            + Command.get_config()
        #print(args)

        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)
    
    @staticmethod
    def inject_node_network_loss(dto):
        (host, names) = (dto['host'], dto['names'])

        args = Command.get_command('node_injection', 'network_loss') \
            + Command.parser(dto) \
            + Command.get_command('network_interface', 'node_' + names) \
            + Command.get_config()
        
        #print(args)
        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_node_disk(dto):
        host = dto['host']

        args = Command.get_command('node_injection', 'disk_fill') \
            + Command.parser(dto) \
            + Command.get_config()
        
        #print(args)
        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_node_process(dto):
        host = dto['host']

        args = Command.get_command('node_injection', 'process_kill') \
            + Command.parser(dto) \
            + Command.get_config()

        #print(args)
        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_pod_delete_by_label(dto):
        pass

    @staticmethod
    def inject_pod_delete_by_name(dto):
        host = dto['host']

        args = Command.get_command('pod_injection', 'pod_delete') \
            + Command.parser(dto) \
            + Command.get_config()

        #print(args)

        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_pod_network_delay(dto):
        host = dto['host']

        args = Command.get_command('pod_injection', 'pod_network_delay') \
            + Command.parser(dto) \
            + Command.get_config()
        
        r_success_dict = Runner.run_adhoc(host, args)

        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def inject_pod_network_loss(dto):
        host = dto['host']
        
        args = Command.get_command('pod_injection', 'pod_network_loss') \
            + Command.parser(dto) \
            + Command.get_config()

        r_success_dict = Runner.run_adhoc(host, args)
        return Handler.get_stdout_info(r_success_dict)


    @staticmethod
    def inject_pod_network_dns(dto):
        host = dto['host']

        args = Command.get_command('pod_injection', 'pod_network_dns') \
            + Command.parser(dto) \
            + Command.get_config()

        r_success_dict = Runner.run_adhoc(host, args)
        return Handler.get_stdout_info(r_success_dict)

    @staticmethod
    def destroy_injection(dto):
        host = dto['host']

        args = Command.get_command('destroy', 'destroy_injection') \
            + dto['uid']

        r_success_dict = Runner.run_adhoc(host, args)
        return Handler.get_stdout_info(r_success_dict)
        
    
    @staticmethod
    def destroy_all(dto):
        host = dto['host']

        uids = Logger.get_uid_list()
        for uid in uids:
            args = Command.get_command('destroy', 'destroy_injection' ) \
            + uid

            Runner.run_adhoc(host, args)
        
        Logger.clear_uid_file()
        
        return "Destroyed all injections successfully"






        
        
        
        

        
        
        



