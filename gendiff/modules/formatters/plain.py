"""
Plain Formatter Module
Formats the difference into a plain text representation.
"""


def format_plain(diff):
    """
    Formats the difference into a plain text representation.

    Args:
        diff (list): The difference tree.

    Returns:
        str: Text representation of the differences.
    """
    return '\n'.join(format_node(diff))


def format_node(node, path=''):
    """
    Formats each node in the difference tree.
    Generates lines for the plain format.

    Args:
        node (list): A list of changes in the difference tree.
        path (str): The current path in the tree.

    Returns:
        list: A list of formatted strings for each change.
    """
    lines = []
    for item in node:
        key = item['key']
        full_path = f"{path}.{key}" if path else key

        if item['type'] == 'added':
            value = stringify(item['value'])
            lines.append(
                f"Property '{full_path}' was added with value: {value}"
            )
        elif item['type'] == 'removed':
            lines.append(f"Property '{full_path}' was removed")
        elif item['type'] == 'updated':
            old_value = stringify(item['old_value'])
            new_value = stringify(item['new_value'])
            lines.append(
                f"Property '{full_path}' was updated. "
                f"From {old_value} to {new_value}"
            )
        elif item['type'] == 'nested':
            lines.extend(format_node(item['children'], full_path))
    return lines


def stringify(value):
    """
    Converts a value into a representation for the plain format.

    Args:
        value: The value to be converted.

    Returns:
        str: The string representation of the value.
    """
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    if value is None:
        return 'null'
    return value
