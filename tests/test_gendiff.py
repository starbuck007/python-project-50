# pylint: disable=redefined-outer-name

"""
Tests for generate_diff in different formats.
"""


import os
import pytest
from gendiff.gendiff import generate_diff


def get_fixture_path(file_name):
    """Returns the full path to a fixture file."""
    return os.path.join('tests', 'fixtures', file_name)


def get_content(file_name):
    """Loads expected output from a file."""
    file_path = f'tests/fixtures/{file_name}'
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


@pytest.mark.parametrize(
    'file1, file2, format_type, expected_file',
    [
        ('file1.json', 'file2.json', 'stylish', 'expected_stylish_output.txt'),
        ('file1.json', 'file2.json', 'json', 'expected_json_output.json'),
        ('file1.yaml', 'file2.yaml', 'plain', 'expected_plain_output.txt'),
        ('file1.yaml', 'file2.yaml', 'stylish', 'expected_stylish_output.txt'),
        ('file1.yaml', 'file2.yaml', 'json', 'expected_json_output.json'),
    ]
)
def test_generate_diff(file1, file2, format_type, expected_file):
    """Tests generate_diff for different files and formats."""
    file_path1 = get_fixture_path(file1)
    file_path2 = get_fixture_path(file2)

    result = generate_diff(file_path1, file_path2, format_type)

    expected_output = get_content(expected_file)

    assert isinstance(result, str)
    assert result == expected_output
