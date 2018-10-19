import os
import subprocess
import sys

import aaa_compose
from commands import Command


class DockerBuilder(Command):
    COMPOSE_DIR = os.path.dirname(aaa_compose.__file__)

    COMMAND_MAPPER = {
        'start': f'docker-compose -f {COMPOSE_DIR}/compose-aaa.yml up',
        'stop': f'docker-compose -f {COMPOSE_DIR}/compose-aaa.yml stop',
        'shutdown': f'docker-compose -f {COMPOSE_DIR}/compose-aaa.yml rm -fv'
    }

    NAME = 'Docker'

    @classmethod
    def build_parser(mcs, parser):
        docker_group = parser.add_mutually_exclusive_group(required=False)
        docker_group.add_argument('--start', help='Starts the AAA module by performing a docker-compose up',
                                  action='store_true')
        docker_group.add_argument('--stop', help='Stops the AAA module', action='store_true')
        docker_group.add_argument('--shutdown', help='Removes all AAA containers and volumes', action='store_true')
        docker_group.add_argument('--restart', help='Performs the shutdown and start commands', action='store_true')

        return parser

    @classmethod
    def execute(mcs, args):
        arg, *rest = super().execute(args)
        command = mcs.COMMAND_MAPPER[arg]

        try:
            subprocess.run(command.split(' '))
        except KeyboardInterrupt:
            sys.exit()
