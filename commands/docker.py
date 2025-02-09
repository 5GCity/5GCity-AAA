import os
import subprocess
import sys

from commands import Command


class DockerBuilder(Command):
    COMMAND_MAPPER = {
        'build': f'docker-compose -f {Command.COMPOSE_DIR}/compose-aaa.yml build',
        'start': f'docker-compose -f {Command.COMPOSE_DIR}/compose-aaa.yml up -d',
        'stop': f'docker-compose -f {Command.COMPOSE_DIR}/compose-aaa.yml stop',
        'shutdown': f'docker-compose -f {Command.COMPOSE_DIR}/compose-aaa.yml down -v --remove-orphans'
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

    @classmethod
    def execute(mcs, args):
        # Validate all configurations
        if not os.path.exists('./aaa_compose/compose-aaa.yml'):
            sys.exit("Compose YAML not found please run '$ python main.py configuration'")
        if args.start:
            mcs.__validate__(args)
        arg, *rest = super().execute(args)
        command = mcs.COMMAND_MAPPER[arg]

        try:
            subprocess.run(command.split(' '))
        except KeyboardInterrupt:
            sys.exit()

    @classmethod
    def __validate__(mcs, args):
        """
        Validates all needed conditions to use the Docker command
        :param args: The namespace with all arguments
        """
        mcs.__max_map_count__()

    @classmethod
    def __max_map_count__(mcs):
        """
        Validates ElasticSearch mmap count.
        :return:
                When nmap count is invalid exits with a message
        """
        needed_max_map_count = 262144

        with open('/proc/sys/vm/max_map_count') as f:
            max_map_count = int(f.read())

        if max_map_count < needed_max_map_count:
            error_message = """
            ElasticSearch needs mmap counts to be increased please run the following command:

            $ sysctl -w vm.max_map_count=262144

            For more information please visit:
            https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
            """
            sys.exit(error_message)
