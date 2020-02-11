import os
import subprocess
import sys
from getpass import getpass

import bcrypt

from commands import Command
from commands.docker import DockerBuilder
from config import YamlLoader


class Configuration(Command):
    VALUES = {}

    @classmethod
    def build_parser(mcs, parser):
        pass

    @classmethod
    def execute(mcs, args):
        base = YamlLoader.load(f'{mcs.COMPOSE_DIR}/compose-aaa-base.yml')
        mcs.common_config(base)
        mcs.nginx(base)
        mcs.gravitee(base)
        YamlLoader.save(base, f'{mcs.COMPOSE_DIR}/compose-aaa.yml')
        # Ensure Compose ENVs are enforced
        subprocess.run(DockerBuilder.COMMAND_MAPPER["start"].split(' '))

    @classmethod
    def common_config(mcs, base):
        parameters = {
            "SERVER_NAME": "Insert the Dashboard server name to be used with the http protocol."
                           "E.g. IP: http://192.168.1.1 or FQDN: http://5g-dashboard.i2cat.net: ",
            "MONITORING_GRAFANA": "Insert the Grafana monitoring UI server to be used."
                                  "E.g., http://192.168.1.1 or FQDN: http://monitoring.5gcity.com: "
        }

        for key, value in parameters.items():
            val = input(value)
            mcs.VALUES[key] = val

        mcs.dashboard_config(base)

    @classmethod
    def dashboard_config(mcs, base):
        dash_path = input("Insert the Dashboard's full path (e.g. /home/5GCITY/dev/5GCity-Dashboard-new): ")
        if dash_path.endswith("/"):
            dash_path = dash_path[:-1]

        # Validate the folder
        if not os.path.exists(dash_path):
            sys.exit("The provided path don't exist.")
        if not os.path.isdir(dash_path):
            sys.exit("The provided path is not a dir.")

        dockerfile = os.path.join(dash_path, "Dockerfile")
        keycloak_json = os.path.join(dash_path, "public", "keycloak_base.json")
        if not os.path.exists(dockerfile) or not os.path.exists(keycloak_json):
            sys.exit("Dockerfile or public/keycloak_base.json are missing don't exist.")

        with open(keycloak_json, "r") as file:
            kj = file.read()
        with open(os.path.join(dash_path, "public", "keycloak.json"), "w") as file:
            kj = kj.replace("<AUTH_SERVER_URL>", f"{mcs.VALUES['SERVER_NAME']}/auth")
            file.write(kj)

        base["services"]["dashboard"]["build"]["context"] = dash_path

        for enum, _ in enumerate(base["services"]["dashboard"]["build"]["args"]):
            for key in mcs.VALUES.keys():

                if key in base["services"]["dashboard"]["build"]["args"][enum]:
                    base["services"]["dashboard"]["build"]["args"][enum] = \
                        base["services"]["dashboard"]["build"]["args"][
                            enum].replace(key, mcs.VALUES[key], 1)

        for enum, _ in enumerate(base["services"]["dashboard"]["volumes"]):
            base["services"]["dashboard"]["volumes"][enum] = base["services"]["dashboard"]["volumes"][enum].replace(
                "DASH_PATH", dash_path)

    @classmethod
    def gravitee(mcs, base):
        def load_base_yml():
            return YamlLoader.load(f'{mcs.COMPOSE_DIR}/gravitee/api/gravitee_base.yml')

        def save_yaml():
            YamlLoader.save(gravitee_base, f'{mcs.COMPOSE_DIR}/gravitee/api/gravitee.yml')

        def set_pwd():
            username = input("Please provide the admin's username: ")
            while True:
                pwd = getpass(prompt="Please set admin password: ")
                pwd_confirm = getpass(prompt="Please confirm your password: ")
                if pwd != pwd_confirm:
                    print("The password and password confirmation don't match.")
                elif len(pwd) < 5:
                    print("Please provide a password with 5 characters at least")
                else:
                    break

            # Encrypt new password
            hashed = bcrypt.hashpw(pwd.encode("UTF-8"), bcrypt.gensalt(prefix=b"2a")).decode("utf-8")
            users = gravitee_base.get("security").get("providers")[0]
            users["username"] = username
            users["password"] = str(hashed)
            users["users"][0]["username"] = username

        def set_mng_uri():
            env = base["services"]["management_ui"]["environment"][0]
            base["services"]["management_ui"]["environment"][0] = env.replace("SERVER_NAME", mcs.VALUES["SERVER_NAME"])

        print("***Gravitee configuration***")
        gravitee_base = load_base_yml()
        set_pwd()
        save_yaml()
        set_mng_uri()

    @classmethod
    def nginx(mcs, base):
        print("***NGINX configuration***")

        ssl = None
        while ssl not in ["y", "n"]:
            ssl = input("Are you going to use SSL (y/n): ")

        ssl = ssl == "y"  # Convert variable to bool
        folder = 'https' if ssl else 'http'

        # Configure nginx Files
        mcs.nginx_conf(f'{mcs.COMPOSE_DIR}/nginx/{folder}/')
        if ssl == "y":
            print(f"Please put the cert file and private key file on {mcs.COMPOSE_DIR}/nginx/{folder}/cert")
            print("With the names bundle.cert and privatekey.key")

        # Configure compose file
        mcs.nginx_compose(base, ssl)

    @classmethod
    def nginx_conf(mcs, config_folder):

        with open(config_folder + "nginx_base.conf", "r") as file:
            conf = file.read()

            value = mcs.VALUES["SERVER_NAME"].split("//")[1]
            conf = conf.replace(f"@SERVER_NAME", value)

        with open(config_folder + 'nginx.conf', "w") as file:
            file.write(conf)

    @classmethod
    def nginx_compose(mcs, base, ssl):
        nginx = base.get("services").get("nginx-service")

        folder = "./nginx/https/" if ssl else "./nginx/http/"

        nginx["volumes"] = []
        nginx.get("volumes").append(f"{folder}nginx.conf:/etc/nginx/conf.d/aaa.conf")
        if ssl:
            nginx.get("ports").append("443:443")
            nginx.get("volumes").append(f"{folder}cert:/etc/nginx/ssl/cert/")
            nginx.get("volumes").append(
                f"{folder}server_names_hash_bucket_size.conf:/etc/nginx/conf.d/server_names_hash_bucket_size.conf")
