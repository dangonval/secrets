class UnkownSecretId(Exception):
    pass


class Passwords:

    def __init__(self, secrets):
        self._secrets = secrets

    def get(self, secret_id):
        if not secret_id:
            return None
        secrets = self._secrets.all_data
        if secret_id not in secrets:
            raise UnkownSecretId(f'Secret ID "{secret_id}" is not defined')
        return secrets[secret_id]
