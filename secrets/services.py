from copy import deepcopy

from .passwords import Passwords
from .utils import matches, select_keys, load_json


class Services:

    def __init__(self, json_file, secrets, mode, keys=None, keyfile=None):
        self._services = load_json(json_file, keyfile)
        self._passwords = Passwords(secrets, keyfile)
        self._mode = mode
        self._keys = keys

    def _resolve(self, services):
        """Resolve usernameId and passwordId"""
        result = []
        for service in services:
            if 'secretPasswords' in service:
                for password in service['secretPasswords']:
                    password['password'] = self._passwords.get(password['passwordId'])
            if 'usernameId' in service:
                service['username'] = self._passwords.get(service['usernameId'])
            for question in service.get('questions') or []:
                question['answer'] = self._passwords.get(question['answerId'])
            result.append(service)
        return result

    def _compact(self, services):
        if self._mode == 'full':
            return services

        def compact_passwords(passwords):
            return ' / '.join([f"{secret['password']} ({secret['description']})" if secret['description']
                               else secret['password'] for secret in passwords])

        def compact_username(username, user_description):
            return f'{username} ({user_description})' if user_description else username

        result = []
        for service in services:
            extracted = deepcopy(service)
            extracted['secretPasswords'] = compact_passwords(extracted['secretPasswords'])
            extracted['username'] = compact_username(extracted['username'], extracted.get('userDescription'))
            result.append(extracted)
        return result

    @staticmethod
    def _apply_regex(services, regex=None):
        """Given a regular expression, return all services where any field matches"""
        if not regex:
            return services
        result = []
        for service in services:
            if matches(service, regex):
                result.append(service)
        return result

    def _select_keys(self, services):
        return [select_keys(service, self._keys) for service in services]

    def search(self, regex=None, resolve=False):
        services = self._resolve(self._services) if resolve else self._services
        services = self._compact(services)
        services = self._apply_regex(services, regex)
        services = self._select_keys(services)
        return services
