from commands import Command
from config import ConfReader
from gravitee import Gravitee


class GraviteeBuilder(Command):
    NAME = 'keycloak'

    @classmethod
    def build_parser(mcs, parser):
        gravitee_parser = parser.add_argument_group('Gravitee', description='Allows to export or import a given API')

        gravitee_group = gravitee_parser.add_mutually_exclusive_group(required=True)
        gravitee_group.add_argument('--export_api', help='Fully export the given api name')
        gravitee_group.add_argument('--import_api', help='Fully import the given api name')

        gravitee_parser.add_argument('--url',
                                     help='The IP address to perform the operation, '
                                          'by default uses the one selected on the docker file. '
                                          'Must contain the protocol the endpoint and the common slash. '
                                          'E.g. http://localhost:8083/management/',
                                     default=ConfReader().get_docker_service('management_ui', 'MGMT_API_URL'))

    @classmethod
    def execute(mcs, args):
        arg, value = super().execute(args)
        getattr(mcs, arg)(value, args.url)

    @classmethod
    def export_api(mcs, *args):
        g = Gravitee.build(args[1])
        g.export_api(args[0])

    @classmethod
    def import_api(mcs, *args):
        g = Gravitee.build(args[1])
        g.import_api(args[0])
