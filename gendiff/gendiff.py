"""Main module for generating differences between two files."""

from gendiff.parser import get_parsed_content
from gendiff.diff_builder import build_diff
from gendiff.formatters.formatter_selector import format_diff


def generate_diff(file1, file2, format_type="stylish"):
    """
    Generates differences between two files
    and returns them in the specified format.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        format_type (str): Output format (stylish, plain, json).

    Returns:
        str: A string with the differences results.
    """
    data1 = get_parsed_content(file1)
    data2 = get_parsed_content(file2)

    diff = build_diff(data1, data2)
    return format_diff(diff, format_type)
