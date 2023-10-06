import configparser
import logging
import re
from typing import Dict, Optional, Union

logging.basicConfig(level=logging.DEBUG)


class IgnoreDuplicateConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.optionxform = str  # make option names case sensitive

    def _read(self, fp, fpname):
        elements_added = set()
        cursect = None  # current section
        lineno = 0
        e = None  # exception
        optcre = re.compile(
            r'(?P<option>[^:=\s][^:=]*)'
            r'\s*(?P<vi>[:=])\s*'
            r'(?P<value>.*)$'
        )

        for lineno, line in enumerate(fp, start=1):
            if not line.strip() or line.strip().startswith(('#', ';')):
                continue

            if line.startswith('['):
                sectname = line.strip('[]')
                cursect = self._sections.setdefault(sectname, self._dict())
                elements_added.add(sectname)
                optname = None
            elif cursect is not None:
                mo = optcre.match(line)
                if mo:
                    optname, vi, optval = mo.group('option', 'vi', 'value')
                    optname = self.optionxform(optname.rstrip())
                    cursect[optname] = optval.strip()
                    elements_added.add((sectname, optname))

        if e:
            raise e


class IniParser:
    def __init__(self):
        self.config = IgnoreDuplicateConfigParser(interpolation=None)  # Disable interpolation

    def parse_ini(self, ini_content: str) -> Optional[configparser.ConfigParser]:
        if not ini_content:
            logging.error("INI content is empty.")
            return None

        try:
            self.config.read_string(ini_content)
            logging.info("INI content parsed successfully.")
            return self.config
        except configparser.Error as e:
            logging.error(f"Error parsing INI content: {e}")
            return None

    def get_sections_and_options(self) -> Dict[str, Dict[str, Union[str, Dict[str, str]]]]:
        sections_and_options = {section: dict(self.config.items(section)) for section in self.config.sections()}
        
        if 'CTkTabview' in sections_and_options:
            ctk_tabview_options = sections_and_options['CTkTabview']
            categorized_options = {
                'Graphics': {},
                'Shadows': {},
                'Miscellaneous': {}
            }

            for option, value in ctk_tabview_options.items():
                category = self.get_category(option)
                if category:
                    categorized_options[category][option] = value
            
            sections_and_options['CTkTabview'] = categorized_options

        return sections_and_options

    def get_category(self, option: str) -> Optional[str]:
        graphics_keywords = ['Bloom', 'HDR', 'Fog', 'Atmosphere', 'LensFlare', 'DepthOfField', 'AmbientOcclusion', 'Quality', 'AntiAliasing', 'Anisotropy', 'SSR']
        shadows_keywords = ['Shadow']
        miscellaneous_keywords = ['OneFrameThreadLag', 'TriangleOrderOptimization', 'AllowLandscapeShadows', 'AllowStaticLighting', 'EyeAdaptationQuality', 'IndirectLightingCache', 'LightFunctionQuality', 'Preshadow', 'SpotLight', 'TiledDeferredShading', 'AOApplyToStaticIndirect', 'ContactShadows', 'InstanceCulling']

        if any(keyword in option for keyword in graphics_keywords):
            return 'Graphics'
        elif any(keyword in option for keyword in shadows_keywords):
            return 'Shadows'
        elif any(keyword in option for keyword in miscellaneous_keywords):
            return 'Miscellaneous'
        return None

    def update_option_in_all_sections(self, option: str, new_value: str):
        for section in self.config.sections():
            if self.config.has_option(section, option):
                self.config.set(section, option, new_value)

    def get_ini_content(self) -> str:
        return '\n\n'.join(
            [f'[{section}]\n' + '\n'.join([f'{option} = {value}' for option, value in self.config.items(section)])
             for section in self.config.sections()])

    @property
    def sections(self) -> Dict[str, Dict[str, str]]:
        return self.get_sections_and_options()


if __name__ == "__main__":
    parser = IniParser()
    ini_content = """
    [section1]
    option1 = value1
    option2 = value2

    [section2]
    option1 = value3
    option2 = value4
    """

    parser.parse_ini(ini_content)
    print(parser.get_ini_content())
