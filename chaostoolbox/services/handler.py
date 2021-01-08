import sys
import os

sys.path.append('../')
from utils.logger import Logger


class Handler:
    def __init__(self):
        pass

    @staticmethod
    def get_stdout_info(result_dict):
        if len(result_dict) > 0:
            ip = list(result_dict.keys())[0]
            res_info = result_dict[ip]["stdout_lines"]
            Logger.log('info',res_info)
            return res_info
        else:
            return "Injection failed"