import yaml

class Config:
    def __init__(self, file_path: str):
        self._config = self._load_config(file_path)

    def _load_config(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    def get_target_url(self):
        return self._config['target']['url']

    def get_data(self):
        return self._config['target']['data']

    def get_fields(self, item):
        return self._config['target']['data'][item]['fields']

    def get_pagination(self):
        if 'pagination' in self._config['target'].keys():
            return self._config['target']['pagination']
        else:
            return None

    def get_output(self):
        return self._config['output']


