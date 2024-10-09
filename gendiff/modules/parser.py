import json
import yaml


def load_data(file_path):
    if file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            return json.load(file)
    elif file_path.endswith(('.yaml', '.yml')):
        with open(file_path) as file:
            return yaml.safe_load(file)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
