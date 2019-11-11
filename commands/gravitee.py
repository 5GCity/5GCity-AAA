from commands import Command
from config import DockerParser
from gravitee import Gravitee


class GraviteeBuilder(Command):
    NAME = 'keycloak'

    @classmethod
    def build_parser(mcs, parser):
        gravitee_parser = parser.add_argument_group('Gravitee', description='Allows to export or import a given API')

        gravitee_group = gravitee_parser.add_mutually_exclusive_group(required=True)
        gravitee_group.add_argument('--export_api', help='Fully export the given api name')
        gravitee_group.add_argument('--import_api', help='Fully import the given api name')

        gravitee_parser.add_argument('--dev', help="Import an API with dev annotations", action="store_true")

        gravitee_parser.add_argument('--url',
                                     help='The IP address to perform the operation, '
                                          'by default uses the one selected on the docker file. '
                                          'Must contain the protocol the endpoint and the common slash. '
                                          'E.g. http://localhost:8083/management/',
                                     default=None)

    @classmethod
    def execute(mcs, args):
        arg, value = super().execute(args)
        getattr(mcs, arg)(value, args.url, args.dev)

    @classmethod
    def export_api(mcs, *args):
        url_ = DockerParser().get_docker_service('management_ui', 'MGMT_API_URL') if not args[1] else args[1]
        g = Gravitee.build(url_)
        g.export_api(args[0])

    @classmethod
    def import_api(mcs, *args):
        url_ = DockerParser().get_docker_service('management_ui', 'MGMT_API_URL') if not args[1] else args[1]
        g = Gravitee.build(url_)
        g.import_api(args[0], args[2])
