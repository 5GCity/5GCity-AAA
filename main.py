import argparse
import sys

from commands.configuration import Configuration
from commands.docker import DockerBuilder
from commands.gravitee import GraviteeBuilder
from commands.keycloak import KeyCloakBuilder

# === Script Commands ===
COMMANDS = {
    'configuration': Configuration,
    'docker': DockerBuilder,
    'keycloak': KeyCloakBuilder,
    'gravitee': GraviteeBuilder
}


def get_args():
    """
    Argument parser to manage the AAA module
    """
    parser = argparse.ArgumentParser(
        description='Script to manage 5G City AAA')

    subparser = parser.add_subparsers(dest="command")

    for key, value in COMMANDS.items():
        _parser = subparser.add_parser(key)
        value.build_parser(_parser)

    args = parser.parse_args()
    command = args.command
    del args.command
    try:
        COMMANDS[command].execute(args)
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    get_args()
