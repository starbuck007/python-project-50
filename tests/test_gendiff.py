import pytest
from gendiff.modules.gendiff import generate_diff
from gendiff.modules.parser_args import parse_args


def test_parse_args():
    args = parse_args(['file1.json', 'file2.json', '--format', 'FORMAT'])
    assert args.first_file == 'file1.json'
    assert args.second_file == 'file2.json'
    assert args.format == 'FORMAT'


def test_single_file_argument():
    with pytest.raises(SystemExit):
        parse_args(['file1.json'])


def test_generate_diff():
    expected_output = """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""
    result = generate_diff('tests/fixtures/file1.json', 'tests/fixtures/file2.json')
    assert result == expected_output


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        generate_diff('non_existent_file1.json', 'non_existent_file2.json')
