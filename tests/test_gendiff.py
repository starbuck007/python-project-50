import json
import yaml
import pytest
import subprocess
from gendiff.modules.gendiff import generate_diff, build_diff, stylish
from gendiff.modules.parser_args import parse_args
from gendiff.modules.parser import load_data


# Загрузка тестовых данных
@pytest.fixture
def load_data_fixture():
    def _load(file_path):
        if file_path.endswith('.json'):
            with open(file_path) as f:
                return json.load(f)
        elif file_path.endswith('.yaml'):
            with open(file_path) as f:
                return yaml.safe_load(f)
    return _load


# Общий ожидаемый diff для всех форматов
@pytest.fixture
def expected_diff():
    return [
        {
            'key': 'common', 'type': 'nested', 'children': [
                {'key': 'follow', 'type': 'added', 'value': False},
                {'key': 'setting1', 'type': 'unchanged', 'value': 'Value 1'},
                {'key': 'setting2', 'type': 'removed', 'value': 200},
                {'key': 'setting3', 'type': 'updated', 'old_value': True, 'new_value': None},
                {'key': 'setting4', 'type': 'added', 'value': 'blah blah'},
                {'key': 'setting5', 'type': 'added', 'value': {'key5': 'value5'}},
                {'key': 'setting6', 'type': 'nested', 'children': [
                    {'key': 'doge', 'type': 'nested', 'children': [
                        {'key': 'wow', 'type': 'updated', 'old_value': '', 'new_value': 'so much'},
                    ]},
                    {'key': 'key', 'type': 'unchanged', 'value': 'value'},
                    {'key': 'ops', 'type': 'added', 'value': 'vops'},
                ]},
            ],
        },
        {
            'key': 'group1', 'type': 'nested', 'children': [
                {'key': 'baz', 'type': 'updated', 'old_value': 'bas', 'new_value': 'bars'},
                {'key': 'foo', 'type': 'unchanged', 'value': 'bar'},
                {'key': 'nest', 'type': 'updated', 'old_value': {'key': 'value'}, 'new_value': 'str'},
            ],
        },
        {'key': 'group2', 'type': 'removed', 'value': {'abc': 12345, 'deep': {'id': 45}}},
        {'key': 'group3', 'type': 'added', 'value': {'deep': {'id': {'number': 45}}, 'fee': 100500}},
    ]


# Общий ожидаемый результат для stylish
@pytest.fixture
def expected_stylish_output():
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


# Тесты для load_data
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
    assert load_data_fixture(file_path) == expected_data


# Тесты для parse_args
@pytest.mark.parametrize("args, expected", [
    (["file1.json", "file2.json", "--format", "stylish"], {"first_file": "file1.json", "second_file": "file2.json", "format": "stylish"}),
    (["file1.json", "file2.json"], {"first_file": "file1.json", "second_file": "file2.json", "format": "stylish"})
])
def test_parse_args_valid(args, expected):
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
    with pytest.raises(SystemExit):
        parse_args(args)


# Тесты для build_diff
@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml")
])
def test_build_diff(file1, file2, load_data_fixture, expected_diff):
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    actual_diff = build_diff(data1, data2)
    assert actual_diff == expected_diff


def test_build_diff_empty_dicts():
    result = build_diff({}, {})
    assert result == []


# Тесты для generate_diff
@pytest.mark.parametrize("file1, file2, format_type, expected_output", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json", "stylish", "stylish"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml", "stylish", "stylish"),
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json", "json", "json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml", "json", "json"),
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json", "yaml", "yaml"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml", "yaml", "yaml"),
])
def test_generate_diff(file1, file2, format_type, expected_output, load_data_fixture, expected_stylish_output, expected_diff):
    result = generate_diff(file1, file2, format_type)
    if format_type == "stylish":
        expected = expected_stylish_output
    elif format_type == "json":
        expected = json.dumps(expected_diff, indent=4)
    elif format_type == "yaml":
        expected = yaml.dump(expected_diff, sort_keys=False)
    else:
        raise ValueError(f"Unknown format type: {format_type}")
    assert result.strip() == expected.strip()


@pytest.mark.parametrize("format_type, expected_type", [
    ("stylish", str),
    ("yaml", str),
    ("json", list)
])
def test_generate_diff_formats(format_type, expected_type):
    result = generate_diff("tests/fixtures/file1.json", "tests/fixtures/file2.json", format_type)
    if format_type == "json":
        parsed = json.loads(result)
        assert isinstance(parsed, expected_type)
    else:
        assert isinstance(result, str)


def test_generate_diff_invalid_format():
    with pytest.raises(ValueError, match="Unsupported format"):
        generate_diff("tests/fixtures/file1.json", "tests/fixtures/file2.json", "xml")


# Тесты для stylish
@pytest.mark.parametrize("file1, file2", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
    ("tests/fixtures/file1.yaml", "tests/fixtures/file2.yaml"),
])
def test_stylish(file1, file2, load_data_fixture, expected_stylish_output):
    data1 = load_data_fixture(file1)
    data2 = load_data_fixture(file2)
    diff = build_diff(data1, data2)
    result = stylish(diff)
    assert result.strip() == expected_stylish_output.strip()


# Тесты CLI
@pytest.mark.parametrize("file1, file2, format_type", [
    ("tests/fixtures/file1.json", "tests/fixtures/file2.json", "stylish"),
])
def test_cli(file1, file2, format_type):
    result = subprocess.run(
        ['python', '-m', 'gendiff.scripts.gendiff', file1, file2, '--format', format_type],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() != ""


@pytest.mark.parametrize("args, expected_code", [
    ([], 2),
    (["file1.json"], 2),
    (["file1.json", "file2.json", "--format", "invalid"], 2),
])
def test_cli_errors(args, expected_code):
    result = subprocess.run(
        ['python', '-m', 'gendiff.scripts.gendiff'] + args,
        capture_output=True,
        text=True
    )
    assert result.returncode == expected_code
