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
from gendiff.modules.parser_args import parse_args


@pytest.fixture
def load_data_fixture():
    """
    Fixture for loading test data from JSON or YAML files.

    Returns:
        function: A function that takes a file path and returns its parsed content.
    """
    def _load(file_path):
        """
        Loads data from the given file path.

        Args:
            file_path (str): Path to the file to load.

        Returns:
            dict: Parsed content of the file.

        Raises:
            ValueError: If the file format is unsupported.
        """
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
    """
    Fixture providing a pre-defined difference tree (diff) for testing.

    Returns:
        list: A diff tree with the differences between two files.
    """
    return [
        {
            'key': 'common',
            'type': 'nested',
            'children': [
                {
                    'key': 'follow',
                    'type': 'added',
                    'value': False
                },
                {
                    'key': 'setting1',
                    'type': 'unchanged',
                    'value': 'Value 1'
                },
                {
                    'key': 'setting2',
                    'type': 'removed',
                    'value': 200
                },
                {
                    'key': 'setting3',
                    'type': 'updated',
                    'old_value': True,
                    'new_value': None
                },
                {
                    'key': 'setting4',
                    'type': 'added',
                    'value': 'blah blah'
                },
                {
                    'key': 'setting5',
                    'type': 'added',
                    'value':
                        {
                            'key5': 'value5'
                        }
                },
                {
                    'key': 'setting6',
                    'type': 'nested',
                    'children': [
                    {
                        'key': 'doge',
                        'type': 'nested',
                        'children': [
                        {
                            'key': 'wow',
                            'type': 'updated',
                            'old_value': '',
                            'new_value': 'so much'
                        },
                    ]
                    },
                    {
                        'key': 'key',
                        'type': 'unchanged',
                        'value': 'value'
                    },
                    {
                        'key': 'ops',
                        'type': 'added',
                        'value': 'vops'
                    },
                ]
                },
            ],
        },
        {
            'key': 'group1',
            'type': 'nested',
            'children': [
                {
                    'key': 'baz',
                    'type': 'updated',
                    'old_value': 'bas',
                    'new_value': 'bars'
                },
                {
                    'key': 'foo',
                    'type': 'unchanged',
                    'value': 'bar'
                },
                {
                    'key': 'nest',
                    'type': 'updated',
                    'old_value':
                        {
                            'key': 'value'
                        },
                    'new_value': 'str'
                },
            ],
        },
        {
            'key': 'group2',
            'type': 'removed',
            'value':
                {
                    'abc': 12345,
                    'deep':
                        {
                            'id': 45
                        }
                }
        },
        {
            'key': 'group3',
            'type': 'added',
            'value':
                {
                    'deep':
                        {
                            'id':
                                {
                                    'number': 45
                                }
                        },
                    'fee': 100500
                }
        },
    ]


@pytest.fixture
def expected_stylish_output():
    """
    Fixture providing the expected output of the 'stylish' formatter.

    Returns:
        str: The expected stylish format output as a string.
    """
    return """{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}"""


@pytest.fixture
def expected_plain_output():
    """
    Fixture providing the expected output of the 'plain' formatter.

    Returns:
        str: The expected plain format output as a string.
    """
    return (
        "Property 'common.follow' was added with value: false\n"
        "Property 'common.setting2' was removed\n"
        "Property 'common.setting3' was updated. From true to null\n"
        "Property 'common.setting4' was added with value: 'blah blah'\n"
        "Property 'common.setting5' was added with value: [complex value]\n"
        "Property 'common.setting6.doge.wow' was updated. From '' to 'so much'\n"
        "Property 'common.setting6.ops' was added with value: 'vops'\n"
        "Property 'group1.baz' was updated. From 'bas' to 'bars'\n"
        "Property 'group1.nest' was updated. From [complex value] to 'str'\n"
        "Property 'group2' was removed\n"
        "Property 'group3' was added with value: [complex value]"
    )


@pytest.mark.parametrize("file_path, expected_data", [
    ("tests/fixtures/file1.json", {
        "common": {
            "setting1": "Value 1",
            "setting2": 200,
            "setting3": True,
            "setting6": {"key": "value", "doge": {"wow": ""}}
        },
        "group1": {"baz": "bas", "foo": "bar", "nest": {"key": "value"}},
        "group2": {"abc": 12345, "deep": {"id": 45}}
    }),
    ("tests/fixtures/file2.yaml", {
        "common": {
            "follow": False,
            "setting1": "Value 1",
            "setting3": None,
            "setting4": "blah blah",
            "setting5": {"key5": "value5"},
            "setting6": {"key": "value", "ops": "vops", "doge": {"wow": "so much"}}
        },
        "group1": {"foo": "bar", "baz": "bars", "nest": "str"},
        "group3": {"deep": {"id": {"number": 45}}, "fee": 100500}
    })
])
def test_load_data(file_path, expected_data, load_data_fixture):
    """
    Tests the data loading function with various file formats.

    Args:
        file_path (str): Path to the test file to load.
        expected_data (dict): Expected parsed data from the file.
        load_data_fixture (function): Fixture for loading the file content.

    Asserts:
        The loaded data matches the expected parsed data.
    """
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
    """
    Tests the parse_args function with valid arguments.

    Args:
        args (list): Command-line arguments to parse.
        expected (dict): Expected parsed arguments with keys:
            - 'first_file': The first file path.
            - 'second_file': The second file path.
            - 'format': The output format (default is 'stylish').

    Asserts:
        The parsed arguments match the expected dictionary values.
    """
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
    """
    Tests the parse_args function with invalid arguments:
    - Required arguments are missing.
    - An invalid format is provided.

    Args:
        args (list): Command-line arguments to parse.

    Asserts:
        The function raises a `SystemExit` exception for invalid input.
    """
    with pytest.raises(SystemExit):
        parse_args(args)


@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml")
])
def test_build_diff(file1, file2, load_data_fixture, expected_diff):
    """
    Tests the build_diff function to ensure it generates the correct diff tree.

    Args:
        file1 (str): Path to the first test file.
        file2 (str): Path to the second test file.
        load_data_fixture (function): Fixture for loading file content.
        expected_diff (list): The expected diff tree describing the differences.

    Asserts:
        The generated diff tree matches the expected diff tree.
    """
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    actual_diff = build_diff(data1, data2)
    assert actual_diff == expected_diff


def test_build_diff_empty_dicts():
    """
    Tests the build_diff function with two empty dictionaries.

    Asserts:
        The generated diff tree is an empty list.
    """
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
    """
    Tests the generate_diff function for different formats.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        format_type (str): Format type ("stylish", "plain").
        expected_fixture (str): Name of the fixture holding the expected output.

    Asserts:
        The generated output matches the expected output for the given format.
    """
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
