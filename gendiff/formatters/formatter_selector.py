"""Module for selecting the formatter for diffs."""

from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import stylish
from gendiff.formatters.json_formatter import format_json


def format_diff(diff, format_type):
    """Formats the difference in the specified format."""
    if format_type == "plain":
        return format_plain(diff)
    if format_type == "stylish":
        return stylish(diff)
    if format_type == "json":
        return format_json(diff)
    raise ValueError(f"Unsupported format: {format_type}")
