from .utils import load_json


class UnkownPasswordId(Exception):
    pass


class Passwords:

    def __init__(self, secrets, keyfile=None):
        self._passwords = load_json(secrets, keyfile)

    def get(self, password_id):
        if not password_id:
            return None
        if password_id not in self._passwords:
            raise UnkownPasswordId(f'Password ID "{password_id}" is not defined')
        return self._passwords[password_id]
