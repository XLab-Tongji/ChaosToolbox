# -*- coding: utf-8 -*


class StressSignalStatementManagement(object):
    def __init__(self):
        pass

    signals = []

    @classmethod
    def get_signals(cls):
        return cls.signals

    @classmethod
    def add_signal(cls, ip, position):
        new_signal = {
            "ip": ip,
            "position": position,
            "state": True
        }
        cls.signals.append(new_signal)
        return len(cls.signals) - 1

    @classmethod
    def change_signal(cls, index):
        cls.signals[index]["state"] = False

    @classmethod
    def stop_special_attacking(cls, ip, position):
        for i in range(0, len(cls.signals)):
            if cls.signals[i]["ip"] == ip and cls.signals[i]["position"] == position:
                cls.signals[i]["state"] = False

    @classmethod
    def stop_all_attacking_to_one(cls, ip):
        for i in range(0, len(cls.signals)):
            if cls.signals[i]["ip"] == ip:
                cls.signals[i]["state"] = False

    @classmethod
    def stop_all_attacking(cls):
        for i in range(0, len(cls.signals)):
            cls.signals[i]["state"] = False

    @classmethod
    def stop_one_attacking(cls, index):
        if index < len(cls.signals):
            cls.signals[index]["state"] = False
            return "succeed"
        else:
            return "invalid index"
