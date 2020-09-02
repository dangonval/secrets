import re
import json

from prettytable import PrettyTable
from cryptography.fernet import Fernet


def matches(data, regex):
    """
    Returns True if the given regex matches any value in the data dictionary.
    Supports embedded lists / dictionaries
    """
    if not data:
        return False
    elif isinstance(data, list):
        for entry in data:
            if matches(entry, regex):
                return True
    elif isinstance(data, str):
        if re.search(regex, data):
            return True
    elif isinstance(data, dict):
        for key, value in data.items():
            if matches(value, regex):
                return True
    return False


def select_keys(data, keys=None):
    """Given a dictionary and some keys, return a new dictionary with the selected keys/values"""
    if not keys:
        return data
    return {key: value for key, value in data.items() if key in keys}


def extract_values(data, keys):
    """Given a dictionary and a list of field names, return a list of values"""
    return [data[key] for key in keys]


def detect_keys(entry):
    return list(entry.keys())


def as_pretty_table(data, field_names=None, **kwargs):
    field_names = field_names or detect_keys(data[0]) if data else None
    table = PrettyTable(field_names, **kwargs)
    for entry in data:
        row = extract_values(entry, field_names)
        table.add_row(row)
    table.align = 'l'
    return table


def get_key():
    key = Fernet.generate_key()
    return key.decode()


def encrypt_with_keyfile(data: str, keyfile=None):
    """Uses the key in the keyfile to encrypt the data"""
    if not keyfile:
        return data
    fernet = Fernet(open(keyfile, 'rb').read())
    return fernet.encrypt(data.encode()).decode()


def decrypt_with_keyfile(data: str, keyfile=None):
    if not keyfile:
        return data
    fernet = Fernet(open(keyfile, 'rb').read())
    return fernet.decrypt(data.encode()).decode()


def load_json(json_file, keyfile=None):
    """Loads a json file. If the keyfile is provided, it is used to decrypt the file before parsing the json content"""
    content = open(json_file).read()
    content = decrypt_with_keyfile(content, keyfile)
    return json.loads(content)


def save_json(data, json_file, keyfile=None):
    content = json.dumps(data)
    content = encrypt_with_keyfile(content, keyfile)
    open(json_file, 'w').write(content)
