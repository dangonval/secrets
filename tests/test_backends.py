import pytest
import json

from secrets.backends import JsonBackend


@pytest.mark.parametrize('services, keyfile, expected', [
    ('tests/expected/services.json', None, 'tests/expected/services.json'),
])
def test_json_backend(services, keyfile, expected):
    services = JsonBackend(services, keyfile)
    assert services.all_data == json.loads(open(expected).read())
