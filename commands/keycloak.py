# TODO: Allow import all realms based on path
# TODO: Allow export all realms on keycloack
from commands import Command
from keycloack import KeyCloak


class KeyCloakBuilder(Command):
    NAME = 'keycloak'

    @classmethod
    def build_parser(cls, parser):
        keycloak_group = parser.add_mutually_exclusive_group(required=False)
        keycloak_group.add_argument('--export_realm', help='Export the given realm file to the specified location',
                                    action='store_true')
        keycloak_group.add_argument('--import_realm', help='Import the given realm file from the specified location')

    @classmethod
    def execute(mcs, args):
        arg, value = super().execute(args)
        getattr(mcs, arg)(value)

    @classmethod
    def export_realm(mcs, *args):
        k = KeyCloak.build()
        k.export_realm()

    @classmethod
    def import_realm(mcs, *args):
        k = KeyCloak.build()
        k.import_realm(args[0])
