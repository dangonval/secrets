import pytest

from secrets.utils import matches, select_keys, extract_values, detect_keys, as_pretty_table
from secrets.utils import get_key, encrypt_with_keyfile, decrypt_with_keyfile, load_json, save_json


@pytest.mark.parametrize('data', [
    dict(one='foo', two='bar'),
    dict(one='foo', two=['bar', 'zuck', 3]),
    dict(one='foo', two=dict(bar='bar', zuck=3)),
    dict(one='foo', two='bar', three=2),
])
@pytest.mark.parametrize('regex, expected', [
    ('^fo.*', True),
    ('foo', True),
    ('bar', True),
    ('woof', False),
])
def test_matches(data, regex, expected):
    assert matches(data, regex) is expected


@pytest.mark.parametrize('data, regex, expected', [
    (None, 'foo', False),
    (False, 'foo', False),
    ('', 'foo', False),
    ('foo', 'foo', True),
    (1, 'foo', False),
])
def test_matches_special_cases(data, regex, expected):
    assert matches(data, regex) is expected


@pytest.mark.parametrize('data, keys, expected', [
    (dict(), ['one'], dict()),
    (dict(one='foo', two='bar'), ['one'], dict(one='foo')),
    (dict(one='foo', two='bar'), ['one', 'two'], dict(one='foo', two='bar')),
    (dict(one='foo', two='bar'), None, dict(one='foo', two='bar')),
])
def test_select_keys(data, keys, expected):
    assert select_keys(data, keys) == expected


@pytest.mark.parametrize('data, keys, expected', [
    (dict(), [], []),
    (dict(one='foo', two='bar'), ['one'], ['foo']),
    (dict(one='foo', two='bar'), ['one', 'two'], ['foo', 'bar']),
])
def test_extract_values(data, keys, expected):
    assert extract_values(data, keys) == expected


@pytest.mark.parametrize('data, expected', [
    (dict(one='foo', two='bar'), {'one', 'two'}),
    (dict(), set()),
])
def test_detect_keys(data, expected):
    assert set(detect_keys(data)) == expected


@pytest.mark.parametrize('data, field_names, expected', [
    ([dict(one=1, two=2), dict(one=11, two=22)], ['one', 'two'], 'tests/expected/table1.txt'),
])
def test_as_pretty_table(data, field_names, expected):
    assert as_pretty_table(data, field_names).get_string() == open(expected).read()


def test_get_key():
    key = get_key()
    assert len(key) == 44
    assert isinstance(key, str)
    assert key[-1] == '='


@pytest.mark.parametrize('data, keyfile', [
    ('some-data', 'tests/data/keyfile1'),
    ('some-data', None),
])
def test_encrypt_and_decrypt(data, keyfile):
    assert decrypt_with_keyfile(encrypt_with_keyfile(data, keyfile), keyfile) == data


@pytest.mark.parametrize('json_file, keyfile, expected', [
    ('tests/data/plain.json', None, dict(one='foo', two='bar')),
    ('tests/data/encrypted.json', 'tests/data/keyfile1', dict(one='foo', two='bar')),
])
def test_load_json(json_file, keyfile, expected):
    assert load_json(json_file, keyfile) == expected


@pytest.mark.parametrize('data, keyfile', [
    (dict(one='foo'), None),
    (dict(one='foo'), 'tests/data/keyfile1'),
])
def test_save_json(data, keyfile):
    json_file = 'tests/tmp/some-file.json'
    save_json(data, json_file, keyfile)
    assert load_json(json_file, keyfile) == data
