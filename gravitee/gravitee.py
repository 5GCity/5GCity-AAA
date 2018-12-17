import json
import os
from dataclasses import dataclass
from typing import ClassVar, Dict

import requests
from requests.auth import HTTPBasicAuth

from config import ConfReader


# TODO: Handle Errors
# TODO: Documentation

@dataclass
class Gravitee:
    ENDPOINTS: ClassVar[Dict[str, str]] = {
        'apis': 'apis',
        'apis_deploy': 'apis/{}/deploy',
        'apis_lifecycle': 'apis/{}',

        'export_api': 'apis/{}/export',
        'export_subscriptions': 'apis/{}/subscriptions',
        'export_applications': 'applications/{}',

        'import_api': 'apis/import',
        'import_applications': 'applications',
        'import_subscriptions': 'apis/{}/subscriptions',

        'plans': 'apis/{}/plans'
    }

    username: str
    password: str
    base_url: str

    @classmethod
    def build(cls):
        arguments = ['username', 'password']
        _args = []
        for arg in arguments:
            _args.append(ConfReader().get('gravitee', arg))

        _args.append(ConfReader().get_docker_service('management_ui', 'MGMT_API_URL'))

        instance = Gravitee(*_args)
        for key in instance.ENDPOINTS.keys():
            instance.ENDPOINTS[key] = instance.base_url + instance.ENDPOINTS[key]
        return instance

    @property
    def authentication(self):
        return HTTPBasicAuth(self.username, self.password)

    @staticmethod
    def write_directory(api, create_dir=True):
        path = os.path.join(os.getcwd(), 'gravitee', 'data', api)
        if not os.path.exists(path) and create_dir:
            os.makedirs(path)
        elif not os.path.exists(path):
            raise ValueError("Provided API don't exist")
        return path

    def export_api(self, name):

        def __api_id__():
            # Collect API id
            r = requests.get(self.ENDPOINTS['apis'], params={'name': name}, auth=self.authentication)
            data = r.json()
            if not data:
                raise ValueError("The provided name don't exist")
            return data[0]['id']

        def __api__():
            # Export the API
            r = requests.get(self.ENDPOINTS['export_api'].format(api_id), auth=self.authentication)

            with open(os.path.join(self.write_directory(name), "api.json"), 'w') as f:
                f.write(json.dumps(r.json(), indent=4))

        def __subscriptions__():
            # Export Subscriptions
            r = requests.get(self.ENDPOINTS['export_subscriptions'].format(api_id), auth=self.authentication)
            data = r.json()
            with open(os.path.join(self.write_directory(name), "subscriptions.json"), 'w') as f:
                f.write(json.dumps(data, indent=4))

            return [subscription['application'] for subscription in data['data']]

        def __application__():
            # Export applications
            data = []
            for app in applications:
                r = requests.get(self.ENDPOINTS['export_applications'].format(app), auth=self.authentication)

                to_remove = ('id', 'status', 'created_at', 'updated_at', 'owner')
                app_data = r.json()
                for k in to_remove:
                    app_data.pop(k, None)
                data.append(app_data)

            with open(os.path.join(self.write_directory(name), "applications.json"), 'w') as f:
                f.write(json.dumps(data, indent=4))

        api_id = __api_id__()
        __api__()
        applications = __subscriptions__()
        __application__()

    def import_api(self, name):

        def __api__():
            with open(os.path.join(reading_directory, 'api.json'), 'r') as f:
                data = json.load(f)
            r = requests.post(self.ENDPOINTS['import_api'], auth=self.authentication, json=data)
            return r.json()['id']

        def __application__():
            with open(os.path.join(reading_directory, 'applications.json'), 'r') as f:
                data = json.load(f)

            for app in data:
                requests.post(self.ENDPOINTS['import_applications'], auth=self.authentication, json=app)

        def __subscriptions__():
            with open(os.path.join(reading_directory, 'subscriptions.json'), 'r') as f:
                data = json.load(f)

            for sub in data['data']:
                payload = {
                    'application': self.get_app_by_name(data['metadata'][sub['application']]),
                    'plan': self.get_plan_by_name(api_id, data['metadata'][sub['plan']])
                }

                requests.post(self.ENDPOINTS['import_subscriptions'].format(api_id), auth=self.authentication,
                              params=payload)

        def __start_api__():
            requests.post(self.ENDPOINTS['apis_deploy'].format(api_id), auth=self.authentication)
            requests.post(self.ENDPOINTS['apis_lifecycle'].format(api_id), auth=self.authentication,
                          params={'action': 'START'})

        reading_directory = self.write_directory(name)
        api_id = __api__()
        __application__()
        __subscriptions__()
        __start_api__()

    def get_plan_by_name(self, api, name):
        r = requests.get(self.ENDPOINTS['plans'].format(api), auth=self.authentication,
                         params={'name': name})

        for plan in r.json():
            if plan['name'] == name['name']:
                return plan['id']

    def get_app_by_name(self, name):
        r = requests.get(self.ENDPOINTS['import_applications'], auth=self.authentication)
        for app in r.json():
            if app['name'] == name['name']:
                return app['id']
