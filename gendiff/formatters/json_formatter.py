"""
JSON Formatter Module
Formats the difference into a json representation.
"""

import json


def format_json(diff):
    """
    Formats the difference tree into a JSON representation.

    Args:
        diff (list): The difference tree.

    Returns:
        str: A JSON-formatted string representing the difference tree.
    """
    return json.dumps(diff, indent=4)
