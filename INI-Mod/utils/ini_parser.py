import configparser
import logging

logging.basicConfig(level=logging.INFO)

class IniParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def parse_ini(self, ini_content):
        try:
            self.config.read_string(ini_content)
            logging.info("INI content parsed successfully.")
            return self.config
        except configparser.Error as e:
            logging.error(f"Error parsing INI content: {e}")
            return None
    
    def validate_ini(self, ini_content):
        try:
            self.config.read_string(ini_content)
            if not self.config.sections():
                logging.warning("Invalid INI content: No sections found.")
                return False

            # Example of enhanced validation
            for section in self.config.sections():
                if not self.config.options(section):
                    logging.warning(f"Section {section} has no keys.")
                    return False
            
            logging.info("INI content is valid.")
            return True
        except configparser.Error as e:
            logging.error(f"Error validating INI content: {e}")
            return False
