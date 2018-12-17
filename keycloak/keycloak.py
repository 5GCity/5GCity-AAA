import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Any, ClassVar

import requests

from config import ConfReader


@dataclass
class KeyCloak:
    ENDPOINTS: ClassVar[Dict[str, str]] = {
        'open_id': '/realms/master/protocol/openid-connect/token',
        'realm': '/admin/realms'
    }

    username: str
    password: str
    client_id: str
    base_url: str

    _access_token: Dict[str, Any] = field(init=False, default=None)

    @classmethod
    def build(cls):
        _args = [
            ConfReader().get_docker_service('keycloak', 'KEYCLOAK_USER'),
            ConfReader().get_docker_service('keycloak', 'KEYCLOAK_PASSWORD'),
            'admin-cli',
            ConfReader().get_docker_service('keycloak', 'AAA_AUTH_BASE_URL')
        ]

        instance = KeyCloak(*_args)
        for key in instance.ENDPOINTS.keys():
            instance.ENDPOINTS[key] = instance.base_url + instance.ENDPOINTS[key]
        return instance

    # === Auth methods ===
    @property
    def access_token(self):
        if self._is_token_valid():
            return self._access_token['access_token']
        elif self._is_token_valid(refresh=True):
            self._renew_token()
            return self._access_token['access_token']

        payload = {
            'username': self.username, 'password': self.password, 'client_id': self.client_id, 'grant_type': 'password'
        }
        r = requests.post(self.ENDPOINTS['open_id'], data=payload)

        if r.status_code > 299:
            raise BaseException(f'Invalid return code {r.status_code} with message: {r.text}')
        self._access_token = r.json()
        self._set_token_expiration_dates()
        return self._access_token

    @property
    def auth_header(self):
        return {'Authorization': f'bearer {self.access_token["access_token"]}'}

    def _is_token_valid(self, refresh=False):
        if not self._access_token:
            return False
        token = 'refresh_expires_in' if refresh else 'expires_in'
        return datetime.now() > self._access_token[token]

    def _renew_token(self):
        if not self._is_token_valid(refresh=True):
            return self.access_token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'username': self.username, 'password': self.password, 'client_id': self.client_id,
            'grant_type': 'refresh_token', 'refresh_token': self._access_token['refresh_token']
        }
        r = requests.get(self.ENDPOINTS['open_id'], headers=headers, data=data)
        if r.status_code > 299:
            raise BaseException(f'Invalid return code {r.status_code} with message: {r.text}')
        self._access_token = r.json()
        self._set_token_expiration_dates()

    def _set_token_expiration_dates(self):
        # Set expiration to python datetime objects
        self._access_token['expires_in'] = datetime.now() + timedelta(seconds=self._access_token['expires_in'])
        self._access_token['refresh_expires_in'] = datetime.now() + timedelta(
            seconds=self._access_token['refresh_expires_in'])

    # === Getters ===

    def get_realms(self):
        r = requests.get(self.ENDPOINTS['realm'], headers=self.auth_header)
        if r.status_code > 299:
            raise BaseException(f'Invalid return code {r.status_code} with message: {r.text}')

        return r.json()

    # === Import Methods ===
    def import_realm(self, file):
        with open(file, 'r') as file:
            realm = json.load(file)
        r = requests.post(self.ENDPOINTS['realm'], headers=self.auth_header, json=realm)
        if r.status_code > 299:
            raise BaseException(f'Invalid return code {r.status_code} with message: {r.text}')
        else:
            print(f'Successfully imported realm {realm["realm"]}')

    # === Export Methods ===
    def export_realm(self, folder=None):
        write_directory = os.path.join(folder, 'realms') if folder else 'realms'
        realms = self.get_realms()

        if not os.path.exists(write_directory):
            os.makedirs(write_directory)

        for realm in realms:
            with open(os.path.join(write_directory, f"{realm['realm']}.json"), 'w') as f:
                f.write(json.dumps(realm, indent=4))
