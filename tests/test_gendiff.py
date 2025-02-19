# pylint: disable=redefined-outer-name

"""
This module contains tests for the app, which generates
a difference between two configuration files in various formats.
"""


import json
import pytest
from gendiff.gendiff import generate_diff


@pytest.fixture
def expected_stylish_output():
    """Loads the expected stylish format output from a file."""
    file_path = 'tests/fixtures/expected_stylish_output.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


@pytest.fixture
def expected_plain_output():
    """Loads the expected plain format output from a file."""
    file_path = 'tests/fixtures/expected_plain_output.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


@pytest.fixture
def expected_json_output():
    """Loads the expected JSON output from a file."""
    file_path = 'tests/fixtures/expected_json_output.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


@pytest.mark.parametrize(
    'file1, file2, format_type, expected_fixture',
    [
        (
                'tests/fixtures/file1.json',
                'tests/fixtures/file2.json',
                'stylish',
                'expected_stylish_output'
        ),
        (
                'tests/fixtures/file1.yaml',
                'tests/fixtures/file2.yaml',
                'plain',
                'expected_plain_output'
        ),
    ]
)
def test_generate_diff(file1, file2, format_type, expected_fixture, request):
    """Tests generate_diff function with different formats."""
    expected_output = request.getfixturevalue(expected_fixture)
    result = generate_diff(file1, file2, format_type)
    assert result.strip() == expected_output.strip()


@pytest.mark.parametrize(
    'file1, file2, format_type, expected_type',
    [
        (
                'tests/fixtures/file1.json',
                'tests/fixtures/file2.json',
                'stylish',
                str
        ),
        (
                'tests/fixtures/file1.json',
                'tests/fixtures/file2.json',
                'json',
                dict
        ),
        (
                'tests/fixtures/file1.yaml',
                'tests/fixtures/file2.yaml',
                'plain',
                str
        ),
        (
                'tests/fixtures/file1.yaml',
                'tests/fixtures/file2.yaml',
                'stylish',
                str
        ),
        (
                'tests/fixtures/file1.yaml',
                'tests/fixtures/file2.yaml',
                'json',
                dict
        ),
    ]
)
def test_generate_diff_formats(
        file1, file2, format_type, expected_type, request
):
    """Tests generate_diff for different files  and formats."""
    result = generate_diff(file1, file2, format_type)
    if format_type == 'json':
        expected_output = request.getfixturevalue('expected_json_output')
        parsed = json.loads(result)
        if isinstance(parsed, list):
            parsed = {item['key']: {k: v for k, v in item.items() if k != 'key'}
                      for item in parsed}
        assert isinstance(parsed, expected_type)
        assert parsed == expected_output
    else:
        assert isinstance(result, str)


def test_generate_diff_invalid_format():
    """Tests the generate_diff for unsupported format_type."""
    file_path1 = 'tests/fixtures/file1.json'
    file_path2 = 'tests/fixtures/file2.json'
    with pytest.raises(ValueError, match='Unsupported format'):
        generate_diff(file_path1, file_path2, 'xml')
