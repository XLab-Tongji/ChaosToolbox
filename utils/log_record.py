# coding=utf-8
import logging


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def log(info_type, message):
        # 日志格式化输出
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT,
                            filename='record.log')
        if info_type == "debug":
            logging.info(message)
        elif info_type == 'info':
            logging.info(message)
        elif info_type == 'warning':
            logging.warning(message)
        else:
            logging.error(message)
