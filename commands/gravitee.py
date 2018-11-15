from commands import Command
from gravitee import Gravitee


class GraviteeBuilder(Command):
    NAME = 'keycloak'

    @classmethod
    def build_parser(cls, parser):
        gravitee_group = parser.add_mutually_exclusive_group(required=False)

        # Old import and export methods from the API
        # keycloak_group.add_argument('--export_realm', help='Export the given realm file to the specified location')
        # keycloak_group.add_argument('--import_realm', help='Import the given realm file from the specified location')
        gravitee_group.add_argument('--export_api', help='Fully export the given api name')
        gravitee_group.add_argument('--import_api', help='Fully import the given api name')

    @classmethod
    def execute(mcs, args):
        arg, value = super().execute(args)
        getattr(mcs, arg)(value)

    @classmethod
    def export_api(mcs, *args):
        g = Gravitee.build()
        g.export_api(args[0])

    @classmethod
    def import_api(mcs, *args):
        g = Gravitee.build()
        g.import_api(args[0])
