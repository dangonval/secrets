import pytest

from secrets.services import Services
from secrets.utils import save_json, load_json
from secrets.backends import JsonBackend


@pytest.mark.parametrize('mode, regex, expected', [
    ('full', 'company1', 'tests/expected/search-full.json'),
    ('compact', 'company1', 'tests/expected/search-compact.json'),
])
def test_services(mode, regex, expected):
    services = JsonBackend('tests/expected/services.json')
    secrets = JsonBackend('tests/expected/secrets.json')
    services = Services(services, secrets, mode)
    data = services.search(regex)
    save_json(data, expected)
    assert services.search(regex) == load_json(expected)
