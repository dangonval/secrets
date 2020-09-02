import pytest

from secrets.passwords import Passwords, UnkownPasswordId


@pytest.mark.parametrize('password_id, raises, expected', [
    (False, False, None),
    (None, False, None),
    ('', False, None),
    ('XX01', False, 'someSecret1'),
    ('unknown', True, None),
])
def test_passwords(password_id, raises, expected):
    passwords = Passwords('tests/expected/secrets.json')
    if raises:
        with pytest.raises(UnkownPasswordId):
            passwords.get(password_id)
    else:
        assert passwords.get(password_id) == expected
