"""
Module for reading and parsing files based on file format.
"""


import os
import json
import yaml


def get_file_extension(file_path):
    """Extracts the file extension from file path."""
    return os.path.splitext(file_path)[1][1:]


def parse_data(content, file_extension):
    """Parses raw content based on the file format."""
    if file_extension == 'json':
        return json.loads(content)
    if file_extension in ('yaml', 'yml'):
        return yaml.safe_load(content)
    raise ValueError(f"Unsupported file format: {file_extension}")


def get_parsed_content(file_path):
    """Reads file and parses content"""
    file_extension = get_file_extension(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return parse_data(content, file_extension)
