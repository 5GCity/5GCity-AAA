import configparser
import os

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


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


class DockerParser(metaclass=Singleton):
    """
    Helper class to parse the docker compose yaml.
    This class only parses the generated file from
    the configuration command.
    """
    def __init__(self):
        self.parser = configparser.ConfigParser(allow_no_value=True)
        self.docker_parse = YamlLoader.load('aaa_compose/compose-aaa.yml')

    def get_docker_service(self, service, config, section='environment'):
        for arg in self.docker_parse['services'][service][section]:
            if config in arg:
                return arg.split("=")[1]
        return None


class YamlLoader:
    """
    Class to handle the YAML operations.
    """

    @staticmethod
    def load(name):
        """
        Loads a YAML file.
        :param name: file's path
        :return: YAML file in a dict format.
        """
        if not os.path.isfile(name):
            raise ValueError(f"File {name} does not exists.")
        return yaml.load(open(name), Loader=yaml.Loader)

    @staticmethod
    def save(data, name):
        """
        Saves a dict in a yaml file format.
        :param data: Dict data to store on the file
        :param name: Name of the file to save.
        """
        with open(name, 'w') as file:
            yaml.dump(data, file, Dumper=Dumper)
