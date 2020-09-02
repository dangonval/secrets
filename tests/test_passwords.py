import pytest

from secrets.backends import JsonBackend
from secrets.passwords import Passwords, UnkownSecretId


@pytest.mark.parametrize('secret_id, raises, expected', [
    (False, False, None),
    (None, False, None),
    ('', False, None),
    ('XX01', False, 'someSecret1'),
    ('unknown', True, None),
])
def test_passwords(secret_id, raises, expected):
    passwords = Passwords(JsonBackend('tests/expected/secrets.json'))
    if raises:
        with pytest.raises(UnkownSecretId):
            passwords.get(secret_id)
    else:
        assert passwords.get(secret_id) == expected
