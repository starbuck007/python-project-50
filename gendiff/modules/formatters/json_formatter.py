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
    diff_as_dict = convert_to_dict(diff)
    return json.dumps(diff_as_dict, indent=4)


def convert_to_dict(diff_list):
    """
    Converts the list-based diff tree into a dictionary format.

    Args:
        diff_list (list): The diff tree represented as a list of changes.

    Returns:
        dict: The diff tree represented as a dictionary.
    """
    result = {}
    for item in diff_list:
        key = item['key']
        result[key] = {k: v for k, v in item.items() if k != 'key'}
    return result
