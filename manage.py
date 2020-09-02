import json
import yaml
import csv

import click

from secrets import Services, as_pretty_table, get_key, encrypt_with_keyfile

KEYS_FOR_COMPACT = ['name', 'username', 'secretPasswords']


def print_data(data, style, keyfile=None):
    """Prints the data in the selected style. If a keyfile is given, it is used to encrypt the data"""
    if style == 'json':
        output = json.dumps(data, indent=2)
    elif style == 'yaml':
        output = yaml.dump(data, indent=2, width=200)
    elif style == 'table':
        table = as_pretty_table(data, KEYS_FOR_COMPACT)
        output = table.get_string()
    else:
        raise NotImplemented
    click.echo(encrypt_with_keyfile(output, keyfile) if keyfile else output)


@click.group()
def cli():
    pass


@cli.command()
def generate_key():
    click.echo(get_key())


@cli.command()
@click.option('--services', help='CSV file with services', required=True)
@click.option('--questions', help='CSV file with questions', required=True)
@click.option('--descriptions', help='CSV file with password descriptions', required=True)
@click.option('--style', type=click.Choice(['json', 'yaml', 'table']), help='Output style', default='json')
@click.option('--questions', help='CSV file with questions', required=True)
@click.option('--keyfile', type=click.Path())
def parse_services(services, questions, descriptions, style, keyfile):
    with open(questions, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='§')
        questions_map = {question['id']: question['question'] for question in csvreader}

    with open(descriptions, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='§')
        pwd_descriptions_map = {description['pwdId']: description['description'] for description in csvreader}

    def get_question_text(question_id):
        if question_id not in questions_map:
            raise ValueError(f'QuestionID "{question_id}" not found')
        return questions_map[question_id]

    def get_description(pwd_id, description):
        if description:
            return description
        if pwd_id in pwd_descriptions_map:
            return pwd_descriptions_map[pwd_id]
        return None

    def process_questions(questions_):
        if not questions_:
            return None
        questions_ = questions_.split(' / ')
        processed = []
        for question in questions_:
            question_id, answer_id = question.split(':')
            processed.append({'question': get_question_text(question_id), 'answerId': answer_id, 'answer': answer_id})
        return processed

    def parse_one_service_file(_services, _parsed):
        with open(_services, newline='', encoding='utf-8') as _csvfile:
            _csvreader = csv.DictReader(_csvfile, delimiter='§')
            for service in _csvreader:
                if service['company'] == 'company':
                    continue
                service['username'] = service['usernameId']
                passwords = service['pwdId'].split(' / ')
                descriptions = service['pwdDescriptions'].split(' / ')
                service['secretPasswords'] = [
                    {'passwordId': pwd_id, 'password': pwd_id, 'description': get_description(pwd_id, description)}
                    for pwd_id, description in zip(passwords, descriptions)
                ]
                if 'questions' in service:
                    service['questions'] = process_questions(service['questions'])
                _parsed.append(service)

    parsed = []
    for filename in services.split(','):
        parse_one_service_file(filename, parsed)
    print_data(parsed, style, keyfile)


@cli.command()
@click.option('--secrets', help='CSV file with passwords', required=True)
@click.option('--style', type=click.Choice(['json', 'yaml', 'table']), help='Output style', default='json')
@click.option('--keyfile', type=click.Path())
def parse_secrets(secrets, style, keyfile):
    with open(secrets, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='§')
        parsed = {}
        for secret in csvreader:
            secret_id = secret['id']
            if secret_id == 'id' or secret_id == '###':
                # skip non-data rows
                continue
            if secret_id not in parsed:
                # New secrets are scalars
                parsed[secret_id] = secret['secret']
            else:
                # convert a multiple secret to a list of secrets
                if isinstance(parsed[secret_id], list):
                    parsed[secret_id].append(secret['secret'])
                else:
                    parsed[secret_id] = [parsed[secret_id], secret['secret']]
    print_data(parsed, style, keyfile)


@cli.command()
@click.option('--services', help='Services file definition', default='data/services.json')
@click.option('--secrets', help='Secrets file definition', default='data/secrets.json')
@click.option('--resolve', help='Resolve secrets', is_flag=True)
@click.option('--regex', help='Regex to match')
@click.option('--style', type=click.Choice(['json', 'yaml', 'table']), help='Output style', default='json')
@click.option('--mode', type=click.Choice(['full', 'compact']), help='How to package information', default='full')
@click.option('--keys', help='Keys to display', default=None)
@click.option('--keyfile', type=click.Path())
def list_services(services, secrets, resolve, regex, style, mode, keys, keyfile):
    keys = keys.split(',') if keys else keys
    if not keys and mode == 'compact':
        keys = KEYS_FOR_COMPACT
    result = Services(services, secrets, mode, keys, keyfile).search(regex, resolve)
    print_data(result, style)


if __name__ == '__main__':
    cli()
