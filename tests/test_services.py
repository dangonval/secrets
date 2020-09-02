import pytest

from secrets.services import Services
from secrets.utils import save_json, load_json


@pytest.mark.parametrize('mode, regex, expected', [
    ('full', 'company1', 'tests/expected/search-full.json'),
    ('compact', 'company1', 'tests/expected/search-compact.json'),
])
def test_services(mode, regex, expected):
    services = Services('tests/expected/services.json', 'tests/expected/secrets.json', mode)
    data = services.search(regex)
    save_json(data, expected)
    assert services.search(regex) == load_json(expected)
