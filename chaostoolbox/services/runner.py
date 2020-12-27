import sys
import json
import random


sys.path.append('../')
from ansible_runner import MyAnsible

class Runner:
    def __init__(self):
        pass

    @staticmethod
    def run_adhoc(host, args, module = 'shell', res_type = 'success'):
        r = MyAnsible()

        r.run(
            hosts = host,
            module = module,
            args = args
        )

        result = r.get_result()

        result_dict = result[res_type]

        return result_dict



