# pylint: disable=redefined-outer-name

"""
Tests for generate_diff in different formats.
"""


import json
import pytest
from gendiff.gendiff import generate_diff


@pytest.fixture
def load_expected_output():
    """To load expected output from a file."""
    def _load(file_name, as_json=False):
        file_path = f'tests/fixtures/{file_name}'
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file) if as_json else file.read()
    return _load


@pytest.mark.parametrize(
    'file1, file2, format_type, expected_type, expected_file, as_json',
    [
        ('file1.json', 'file2.json', 'stylish', str,
         'expected_stylish_output.txt', False),
        ('file1.json', 'file2.json', 'json', dict, 'expected_json_output.json',
         True),
        ('file1.yaml', 'file2.yaml', 'plain', str, 'expected_plain_output.txt',
         False),
        ('file1.yaml', 'file2.yaml', 'stylish', str,
         'expected_stylish_output.txt', False),
        ('file1.yaml', 'file2.yaml', 'json', dict, 'expected_json_output.json',
         True),
    ]
)
def test_generate_diff(file1, file2, format_type, expected_type,
                               expected_file, as_json, load_expected_output):
    """Tests generate_diff for different files and formats."""
    file_path1 = f'tests/fixtures/{file1}'
    file_path2 = f'tests/fixtures/{file2}'

    result = generate_diff(file_path1, file_path2, format_type)

    expected_output = load_expected_output(expected_file, as_json=as_json)

    if format_type == 'json':
        parsed = json.loads(result)
        if isinstance(parsed, list):
            parsed = {item['key']: {k: v for k, v in item.items() if k != 'key'}
                      for item in parsed}
        assert isinstance(parsed, expected_type)
        assert parsed == expected_output
    else:
        assert isinstance(result, expected_type)
        assert result.strip() == expected_output.strip()
