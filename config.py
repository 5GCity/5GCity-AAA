import configparser
from ast import literal_eval as le

from importlib_resources import read_text

import etc


class Singleton(type):
    """
    Creates a singleton instance for the parent class.
    This way only one instance will be available throughout the application.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfReader(metaclass=Singleton):
    """
    Read configuration from the ini file
    The class uses the ini_file input to read external or default file
    """

    def __init__(self):
        self.parser = configparser.ConfigParser(allow_no_value=True)
        self.parser.read_string(read_text(etc, 'conf.ini'))

    def get(self, section, config):
        return le(self.parser.get(section, config))

    def get_list(self, section, config):
        return self.parser.get(section, config).split(',')

    def get_section_dict(self, section):
        configs_list = self.parser.items(section, raw=True) if section in self.parser else None
        configs = dict()
        for key, value in configs_list:
            configs[key] = self.get(section, key)
        return configs
