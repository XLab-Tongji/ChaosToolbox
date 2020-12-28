



class Handler:
    def __init__(self):
        pass

    @staticmethod
    def get_stdout_info(result_dict):
        if len(result_dict) > 0:
            ip = list(result_dict.keys())[0]
            res_info = result_dict[ip]["stdout_lines"]
            return res_info
        else:
            return "Injection failed"