import os
import ConfigParser

current_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(current_path, "default_cmd.ini")
conf = ConfigParser.ConfigParser()

conf.read(config_path)

Default_cmd = {
    "cpu": conf.get("Default_cmd", "cpu"),
    "network": conf.get("Default_cmd", "network"),
    "disk": conf.get("Default_cmd", "disk"),
    "mem": conf.get("Default_cmd", "mem"),
    "k8s": conf.get("Default_cmd", "k8s")
}
