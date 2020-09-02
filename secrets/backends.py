from .utils import load_json


class JsonBackend:

    """Data backed by a json file, protected with a keyfile (if given)"""

    def __init__(self, json_file, keyfile=None):
        self._data = load_json(json_file, keyfile)

    @property
    def all_data(self):
        return self._data
