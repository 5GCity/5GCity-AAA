import os
import subprocess
import sys

from commands import Command
from config import DockerParser
from keycloak import KeyCloak


class KeyCloakBuilder(Command):
    NAME = 'keycloak'

    @classmethod
    def build_parser(mcs, parser):
        keycloak_group = parser.add_mutually_exclusive_group(required=False)

        # Old import and export methods from the API
        # keycloak_group.add_argument('--export_realm', help='Export the given realm file to the specified location')
        # keycloak_group.add_argument('--import_realm', help='Import the given realm file from the specified location')
        keycloak_group.add_argument('--export_realm', help='Fully export the given realm name')
        keycloak_group.add_argument('--import_realm', help='Fully import the given realm name')

    @classmethod
    def execute(mcs, args):
        arg, value = super().execute(args)
        getattr(mcs, arg)(value)

    @classmethod
    def export_realm_api(mcs, *args):
        k = KeyCloak.build()
        k.export_realm()

    @classmethod
    def import_realm_api(mcs, *args):
        k = KeyCloak.build()
        k.import_realm(args[0])

    @classmethod
    def __build_docker_command__(mcs, realm_name):
        import docker

        client = docker.from_env()
        postgres = client.containers.list(filters={'name': 'postgresdb'})[0]

        realm_path = os.path.join(os.getcwd(), 'keycloak', 'data', realm_name)

        command = (
            "docker run --rm -it -e USER=$USER -e USERID=$UID --name keycloak_exporter --network=aaa_compose_default "
            f"-v {realm_path}:/tmp/export "
            f"-e DB_DATABASE={DockerParser().get_docker_service('keycloak', 'DB_DATABASE')} "
            f"-e DB_PASSWORD={DockerParser().get_docker_service('keycloak', 'DB_PASSWORD')} "
            f"-e DB_USER={DockerParser().get_docker_service('keycloak', 'DB_USER')} "
            f"-e DB_VENDOR={DockerParser().get_docker_service('keycloak', 'DB_VENDOR')} "
            f"-e DB_ADDR={postgres.attrs['NetworkSettings']['Networks']['aaa_compose_default']['IPAddress']} "
            f"-e DB_PORT={DockerParser().get_docker_service('keycloak', 'DB_PORT')} "
            "jboss/keycloak "
            f"-Dkeycloak.migration.realmName={realm_name} "
            "-Dkeycloak.migration.provider=dir "
            "-Dkeycloak.migration.provider=dir "
            "-Dkeycloak.migration.dir=/tmp/export "
        )

        return realm_path, command

    @classmethod
    def export_realm(mcs, *args):

        # TODO: Auto close process

        realm_path, command = mcs.__build_docker_command__(args[0])
        # Needed to avoid docker permission conflict
        if not os.path.exists(realm_path):
            os.makedirs(realm_path)

        command += (
            "-Dkeycloak.migration.action=export "
            "-Dkeycloak.migration.usersExportStrategy=SAME_FILE"
        )
        try:
            subprocess.call(command.split(' '))
        except KeyboardInterrupt:
            sys.exit()

    @classmethod
    def import_realm(mcs, *args):

        # TODO: Auto close process

        realm_path, command = mcs.__build_docker_command__(args[0])

        if not os.path.exists(realm_path):
            raise ValueError("Provided realm don't exist")

        command += (
            "-Dkeycloak.migration.action=import "
            "-Dkeycloak.migration.strategy=OVERWRITE_EXISTING"
        )
        try:
            subprocess.call(command.split(' '))
        except KeyboardInterrupt:
            sys.exit()
