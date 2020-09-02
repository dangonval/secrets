import os

import pytest
from click.testing import CliRunner

from manage import generate_key, parse_services, parse_secrets, list_services


@pytest.fixture
def generate_csv_files():
    os.system('scripts/extract-org-table.el services tests/data/services.org csv > tests/tmp/services.csv')
    os.system('scripts/extract-org-table.el questions tests/data/services.org csv > tests/tmp/questions.csv')
    os.system('scripts/extract-org-table.el descriptions tests/data/services.org csv > tests/tmp/descriptions.csv')
    os.system('scripts/extract-org-table.el secrets tests/data/secrets.org csv > tests/tmp/secrets.csv')


def test_generate_key():
    runner = CliRunner()
    result = runner.invoke(generate_key)
    assert result.exit_code == 0
    assert result.output[-1] == '\n'


def test_parse_services(generate_csv_files):
    runner = CliRunner()
    result = runner.invoke(parse_services, [
        '--services', 'tests/tmp/services.csv', '--questions', 'tests/tmp/questions.csv',
        '--descriptions', 'tests/tmp/descriptions.csv'])
    assert result.exit_code == 0
    assert result.output == open('tests/expected/services.json').read()


def test_parse_secrets(generate_csv_files):
    runner = CliRunner()
    result = runner.invoke(parse_secrets, ['--secrets', 'tests/tmp/secrets.csv'])
    assert result.exit_code == 0
    assert result.output == open('tests/expected/secrets.json').read()


def test_list_services():
    runner = CliRunner()
    result = runner.invoke(list_services, [
        '--services', 'tests/expected/services.json', '--secrets', 'tests/expected/secrets.json',
        '--resolve', '--style', 'table', '--mode', 'compact'
    ])
    assert result.exit_code == 0
    assert result.output == open('tests/expected/list-services.txt').read()
