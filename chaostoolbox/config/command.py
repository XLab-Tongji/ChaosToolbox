import os
import configparser

'''
This class decodes the ./command.ini file to get commands
'''
class Command:
    def __init__(self):
        pass
    '''
    This function gets all commands
    returns a two dimensional dict whose keys are section_name and option_name
    '''
    @staticmethod
    def get_all_commands():
        # Initialize the config parser
        current_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(current_path, 'command.ini')
        

        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        
        # Get all sections of the config file
        sections = parser.sections()
        
        # Initialize the return dict
        commands={}

        # Traverse the sections and options
        for section in sections:
            
            commands[section] = {}
            options = parser.options(section)
            

            for option in options:
                # There are quotes in the resulting string so slice is used to remove them
                cur = parser.get(section, option)[1:-1]
                commands[section][option] = cur
        
        
        return commands
    
    '''
    This function gets the command by given section_name and option_name
    ret_val : str
    '''
    @staticmethod
    def get_command(section_name, option_name):
        # Initialize the parser
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'command.ini')
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        
        try:
            # There are quotes in the resulting string so slice is used to remove them
            ret_val = parser.get(section_name, option_name)[1:-1]
            
            return ret_val
        except Exception:
            pass
        else:
            return None

            
        


