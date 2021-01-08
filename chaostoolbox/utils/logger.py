import logging
import json

class Logger:
    def __init__(self):
        pass

    @staticmethod
    def log(info_type, message):
        try:
            uid = json.loads(str(message[0]))['result']
            if len(uid) == 16:
                uid_file = open('./chaostoolbox/data/log/uid.log','a')
                uid_file.write(uid + '\n')
                uid_file.close()
        except Exception:
            pass
        # 日志格式化输出
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        #DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT,
                            filename='./chaostoolbox/data/log/record.log')
        if info_type == "debug":
            logging.info(message)
        elif info_type == 'info':
            logging.info(message)
        elif info_type == 'warning':
            logging.warning(message)
        else:
            logging.error(message)

    @staticmethod
    def get_uid_list():
        with open('./chaostoolbox/data/log/uid.log', 'r') as f:
            uids = [line.strip('\n') for line in f] 
            uids.reverse()
            return uids

    @staticmethod
    def clear_uid_file():
        with open('./chaostoolbox/data/log/uid.log', 'w') as f:
            f.close()

        
        
