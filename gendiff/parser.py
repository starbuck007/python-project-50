import json
import yaml


def load_data(file_path):
    """Reads raw content from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def parse_data(content, file_path):
    """Parses raw content based on the file format."""
    if file_path.endswith('.json'):
        return json.loads(content)
    elif file_path.endswith(('.yaml', '.yml')):
        return yaml.safe_load(content)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
