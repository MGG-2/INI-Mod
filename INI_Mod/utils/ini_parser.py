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
        errors = []
        try:
            self.config.read_string(ini_content)
            if not self.config.sections():
                errors.append("No sections found.")
            
            for section in self.config.sections():
                if not self.config.options(section):
                    errors.append(f"Section {section} has no keys.")
            
            if errors:
                logging.warning("Invalid INI content:")
                for error in errors:
                    logging.warning(f"- {error}")
                return False, errors
            
            logging.info("INI content is valid.")
            return True, []
        except configparser.Error as e:
            logging.error(f"Error validating INI content: {e}")
            errors.append(str(e))
            return False, errors
    
    def auto_fix(self, ini_content):
        fixed_content = ini_content.strip()
        if not fixed_content:
            return "[default]\n"

        if not fixed_content.startswith('['):
            fixed_content = "[default]\n" + fixed_content

        return fixed_content
