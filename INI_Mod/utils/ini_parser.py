import configparser
import logging
import re

logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more detailed logging

class IgnoreDuplicateConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super(IgnoreDuplicateConfigParser, self).__init__(*args, **kwargs)
        self.optionxform = str  # make option names case sensitive

    def _read(self, fp, fpname):
        logging.debug(f"Starting to read INI content from {fpname}")
        elements_added = set()
        cursect = None
        optname = None
        lineno = 0
        e = None
        optcre = re.compile(
            r'(?P<option>[^:=\s][^:=]*)'
            r'\s*(?P<vi>[:=])\s*'
            r'(?P<value>.*)$'
        )
        for lineno, line in enumerate(fp, start=1):
            if not line.strip():
                continue
            # comment or blank line?
            if line.strip().startswith('#') or line.strip().startswith(';'):
                continue
            if line.startswith('['):
                if line[line.find('[') + 1:].startswith('['):
                    raise ValueError("Invalid section name format at line %s" % lineno)
                sectname = line.split('[', 1)[1].split(']', 1)[0]
                if sectname in self._sections:
                    if self._strict and sectname in elements_added:
                        raise configparser.DuplicateSectionError(sectname, fpname, lineno)
                    cursect = self._sections[sectname]
                    elements_added.add(sectname)
                elif sectname == configparser.DEFAULTSECT:
                    cursect = self._defaults
                else:
                    cursect = self._dict()
                    cursect['__name__'] = sectname
                    self._sections[sectname] = cursect
                    self._proxies[sectname] = configparser.SectionProxy(self, sectname)
                    elements_added.add(sectname)
                # So sections can't start with a continuation line
                optname = None
            # option line?
            elif cursect is not None:
                mo = optcre.match(line)
                if mo:
                    optname, vi, optval = mo.group('option', 'vi', 'value')
                    if optname in cursect and (sectname, optname) in elements_added:
                        continue  # Ignore the duplicated option
                    if not optname:
                        if line.strip().startswith(('=', ':')):
                            raise ValueError("Option name is required at line %s" % lineno)
                        else:
                            e = self._handle_error(e, fpname, lineno, line)
                    elif optname in cursect:
                        if self._strict and (sectname, optname) in elements_added:
                            raise configparser.DuplicateOptionError(sectname, optname, fpname, lineno)
                        elements_added.add((sectname, optname))
                    optname = self.optionxform(optname.rstrip())
                    # match if it would set optval to None
                    if optval is not None:
                        optval = optval.strip()
                        # Check if this optname already exists
                        if optname in cursect:
                            # If overwriting is allowed, overwrite
                            if self._allow_no_value:
                                cursect[optname] = optval
                            # Otherwise raise an error
                            else:
                                raise configparser.DuplicateOptionError(sectname, optname, fpname, lineno)
                        else:
                            cursect[optname] = optval
                    else:
                        # valueless option handling
                        cursect[optname] = None
        # if any parsing errors occurred, raise an exception
        if e:
            raise e
        logging.debug(f"Starting to read INI content from {fpname}")

class IniParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config = IgnoreDuplicateConfigParser(interpolation=None)  # Disable interpolation
    
    def parse_ini(self, ini_content):
        logging.debug("Parsing INI content:")
        logging.debug(ini_content)
        try:
            self.config.read_string(ini_content)
            logging.info("INI content parsed successfully.")
            logging.debug("Parsed INI content:")
            logging.debug(self.get_ini_content())  # Log the parsed content
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

    def get_sections_and_options(self):
        """
        Retrieve the sections and options from the parsed INI content.

        Returns:
            A dictionary where keys are section names and values are dictionaries of options and their values.
        """
        sections_and_options = {}
        for section in self.config.sections():
            options = {option: self.config.get(section, option) for option in self.config.options(section)}
            sections_and_options[section] = options

        return sections_and_options

    def update_ini_option(self, section, option, value):
        logging.debug(f"Updating INI option {section}.{option} to {value}")
        try:
            self.config.set(section, option, value)
            logging.debug("Option updated successfully.")
            logging.debug("Updated INI content:")
            logging.debug(self.get_ini_content())  # Log the updated content
            return True
        except configparser.Error as e:
            logging.error(f"Error updating INI option: {e}")
            return False

    def get_ini_content(self):
        ini_content = ""
        for section in self.config.sections():
            ini_content += f"[{section}]\n"
            for option in self.config.options(section):
                ini_content += f"{option} = {self.config.get(section, option)}\n"
            ini_content += "\n"
        return ini_content
    
    