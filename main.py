import argparse

from commands.docker import DockerBuilder
from commands.keycloak import KeyCloakBuilder

# TODO: Log and catch exceptions
# TODO: Add gravity export and import functions
# TODO: Provide function documentation and licensing


# === Script Commands ===
COMMANDS = {
    'docker': DockerBuilder,
    'keycloak': KeyCloakBuilder
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
    COMMANDS[command].execute(args)


if __name__ == '__main__':
    get_args()
