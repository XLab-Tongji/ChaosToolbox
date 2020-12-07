import os
import configparser

class Command:
    def __init__(self):
        pass

    @staticmethod
    def get_all_commands():
        current_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(current_path, 'command.ini')
        
        os.chdir(current_path)

        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        
        sections = parser.sections()
        
        commands={}

        for section in sections:
            
            commands[section] = {}
            options = parser.options(section)
            

            for option in options:
                #There are quotes in the resulting string so slice is used to remove them
                cur = parser.get(section, option)[1:-1]
                commands[section][option] = cur
        
        #print(commands)
        return commands
                
    @staticmethod
    def get_command(section_name, option_name):
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'command.ini')
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        
        try:
            #There are quotes in the resulting string so slice is used to remove them
            ret_val = parser.get(section_name, option_name)[1:-1]
            
            return ret_val
        except Exception:
            pass
        else:
            return None

            
        


