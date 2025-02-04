# pylint: disable=redefined-outer-name

"""
This module contains tests for the app, which generates
a difference between two configuration files in various formats.
"""
import subprocess
import json
import yaml
import pytest
from gendiff.modules.gendiff import generate_diff, build_diff, stylish
from gendiff.modules.formatters.plain import stringify, format_plain
from gendiff.modules.formatters.json_formatter import format_json
from gendiff.modules.parser_args import parse_args


@pytest.fixture
def load_data_fixture():
    """Loads test data from JSON or YAML files."""
    def _load(file_path):
        if file_path.endswith('.json'):
            with open(file_path, encoding='utf-8') as f:
                return json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            with open(file_path, encoding='utf-8') as f:
                return yaml.safe_load(f)
        raise ValueError(f"Unsupported file format: {file_path}")
    return _load


@pytest.fixture
def expected_diff():
    """Loads the expected diff tree from a file."""
    file_path = 'tests/fixtures/expected_diff.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


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


@pytest.mark.parametrize("file_path, expected_file", [
    ("tests/fixtures/file1.json", "tests/fixtures/expected_file1.json"),
    ("tests/fixtures/file2.yaml", "tests/fixtures/expected_file2.yaml")
])
def test_load_data(file_path, expected_file, load_data_fixture):
    """Tests the data loading function with various file formats."""
    with open(expected_file, 'r', encoding='utf-8') as file:
        expected_data = (
            json.load(file) if expected_file.endswith('.json')
            else yaml.safe_load(file)
        )
    assert load_data_fixture(file_path) == expected_data


@pytest.mark.parametrize(
    "args, expected",
    [
        (
                ["file1.json", "file2.json", "--format", "stylish"],
                {
                    "first_file": "file1.json",
                    "second_file": "file2.json",
                    "format": "stylish"
                }
        ),
        (
                ["file1.json", "file2.json"],
                {
                    "first_file": "file1.json",
                    "second_file": "file2.json",
                    "format": "stylish"
                }
        )
    ]
)
def test_parse_args_valid(args, expected):
    """Tests parse_args with valid arguments"""
    parsed_args = parse_args(args)
    assert parsed_args.first_file == expected["first_file"]
    assert parsed_args.second_file == expected["second_file"]
    assert parsed_args.format == expected["format"]


@pytest.mark.parametrize("args", [
    (["file1.json"]),
    ([]),
    (["file1.json", "file2.json", "--format", "invalid_format"])
])
def test_parse_args_invalid(args):
    """Tests parse_args with invalid arguments"""
    with pytest.raises(SystemExit):
        parse_args(args)


@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml")
])
def test_build_diff(file1, file2, load_data_fixture, expected_diff):
    """Tests build_diff with correct diff tree."""
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    actual_diff = build_diff(data1, data2)
    assert actual_diff == expected_diff


def test_build_diff_empty_dicts():
    """Tests build_diff with empty dictionaries."""
    result = build_diff({}, {})
    assert not result


@pytest.mark.parametrize(
    "file1, file2, format_type, expected_fixture",
    [
        (
                "tests/fixtures/file1.json",
                "tests/fixtures/file2.json",
                "stylish",
                "expected_stylish_output"
        ),
        (
                "tests/fixtures/file1.yaml",
                "tests/fixtures/file2.yaml",
                "plain",
                "expected_plain_output"
        ),
    ]
)
def test_generate_diff(file1, file2, format_type, expected_fixture, request):
    """Tests generate_diff function with different formats."""
    expected_output = request.getfixturevalue(expected_fixture)
    result = generate_diff(file1, file2, format_type)
    assert result.strip() == expected_output.strip()


@pytest.mark.parametrize("format_type, expected_type", [
    ("stylish", str),
])
def test_generate_diff_formats(format_type, expected_type):
    """
    Tests the generate_diff function for supported formats.

    Args:
        format_type (str): The format type to test ("stylish", "json", etc.).
        expected_type (type): The expected data type of the generated output.

    Asserts:
        The output of the `generate_diff` function matches the expected type.
    """
    result = generate_diff("tests/fixtures/file1.json", "tests/fixtures/file2.json", format_type)
    if format_type == "json":
        parsed = json.loads(result)
        assert isinstance(parsed, expected_type)
    else:
        assert isinstance(result, str)


def test_generate_diff_invalid_format():
    """
    Tests the generate_diff function with an unsupported format.

    Asserts:
        A `ValueError` is raised with the message "Unsupported format" when
        an invalid format type is used.
    """
    with pytest.raises(ValueError, match="Unsupported format"):
        generate_diff("tests/fixtures/file1.json", "tests/fixtures/file2.json", "xml")


@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml"),
])
def test_stylish(file1, file2, load_data_fixture, expected_stylish_output):
    """
    Tests the stylish formatter with JSON and YAML input files.

    Args:
        file1 (str): Path to the first test file (JSON or YAML).
        file2 (str): Path to the second test file (JSON or YAML).
        load_data_fixture (function): Fixture for loading file content.
        expected_stylish_output (str): The expected output in stylish format.

    Asserts:
        The output of the `stylish` function matches the expected output.
    """
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    diff = build_diff(data1, data2)
    result = stylish(diff)
    assert result.strip() == expected_stylish_output.strip()


def test_stringify():
    """
    Tests the stringify function for various input types.

    Asserts:
        Output matches the expected format for each input type.
    """
    assert stringify(True) == 'true'
    assert stringify(False) == 'false'
    assert stringify(None) == 'null'
    assert stringify("string") == "'string'"
    assert stringify(123) == 123
    assert stringify({"key": "value"}) == "[complex value]"


@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml"),
])
def test_format_plain(file1, file2, load_data_fixture, expected_plain_output):
    """
    Tests the plain formatter with JSON and YAML input files.

    Args:
        file1 (str): Path to the first test file (JSON or YAML).
        file2 (str): Path to the second test file (JSON or YAML).
        load_data_fixture (function): Fixture for loading file content.
        expected_plain_output (str): The expected output in plain format.

    Asserts:
        The output of the `format_plain` function matches the expected plain output.
    """
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    diff = build_diff(data1, data2)
    result = format_plain(diff)
    assert result == expected_plain_output


@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
])
def test_format_json(file1, file2, load_data_fixture, expected_json_output):
    """
    Tests the JSON formatter function.

    Args:
        file1 (str): Path to the first test file.
        file2 (str): Path to the second test file.
        load_data_fixture (function): Fixture for loading file content.
        expected_json_output (str): The expected JSON output for the comparison.

    Asserts:
        - The JSON output matches the expected formatted result.
    """
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    diff = build_diff(data1, data2)
    result = format_json(diff)
    expected_json = json.dumps(expected_json_output, indent=4)
    assert result == expected_json


@pytest.mark.parametrize("file1, file2, format_type", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json", "stylish"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml", "plain"),
])
def test_cli(file1, file2, format_type):
    """
    Tests the command-line interface (CLI).

    Args:
        file1 (str): Path to the first file to compare.
        file2 (str): Path to the second file to compare.
        format_type (str): The format type for the output ("stylish", "plain").

    Asserts:
        - The CLI exits with a return code of 0 (successful execution).
        - The standard output (stdout) is not empty.
    """
    result = subprocess.run(
        ['python', '-m', 'gendiff.scripts.gendiff', file1, file2, '--format', format_type],
        capture_output=True, text=True, check=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() != ""


@pytest.mark.parametrize("args, expected_code", [
    ([], 2),
    (["file1.json"], 2),
    (["file1.json", "file2.json", "--format", "invalid"], 2),
])
def test_cli_errors(args, expected_code):
    """
    Tests error handling in the command-line interface (CLI).

    Args:
        args (list): Command-line arguments to pass to the CLI.
        expected_code (int): The expected return code for the given arguments.

    Asserts:
        - The CLI exits with the expected error code.
    """
    result = subprocess.run(
        ['python', '-m', 'gendiff.scripts.gendiff'] + args,
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == expected_code
