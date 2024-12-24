"""
Stylish Formatter Module
Formats the difference into a stylish representation.
"""


def format_value(value, depth):
    """
    Converts a value into a representation for the stylish format.

    Args:
        value: The value to be converted.
        depth (int): The current depth level in the nested structure.

    Returns:
        str: The string representation of the value.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        indent = "    " * (depth + 1)
        closing_indent = "    " * depth
        lines = [
            f"{indent}{key}: {format_value(val, depth + 1)}"
            for key, val in value.items()
        ]
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"
    else:
        return str(value)


def format_added(indent, key, value, depth):
    """
        Formats a node representing an added property in the stylish format.

        Args:
            indent (str): The current indentation string.
            key (str): The key of the added property.
            value: The value of the added property.
            depth (int): The current depth level in the nested structure.

        Returns:
            str: The formatted string representing the added property.
        """
    return f"{indent}  + {key}: {format_value(value, depth + 1)}"


def format_removed(indent, key, value, depth):
    """
        Formats a node representing a removed property in the stylish format.

        Args:
            indent (str): The current indentation string.
            key (str): The key of the removed property.
            value: The value of the removed property.
            depth (int): The current depth level in the nested structure.

        Returns:
            str: The formatted string representing the removed property.
        """
    return f"{indent}  - {key}: {format_value(value, depth + 1)}"


def format_unchanged(indent, key, value, depth):
    """
        Formats a node representing an unchanged property in the stylish format.

        Args:
            indent (str): The current indentation string.
            key (str): The key of the unchanged property.
            value: The value of the unchanged property.
            depth (int): The current depth level in the nested structure.

        Returns:
            str: The formatted string representing the unchanged property.
        """
    return f"{indent}    {key}: {format_value(value, depth + 1)}"


def format_updated(indent, key, old_value, new_value, depth):
    """
        Formats a node representing an updated property in the stylish format.

        Args:
            indent (str): The current indentation string.
            key (str): The key of the updated property.
            old_value: The old value of the property.
            new_value: The new value of the property.
            depth (int): The current depth level in the nested structure.

        Returns:
            list: The list of two formatted strings with the old and new values.
        """
    return [
        f"{indent}  - {key}: {format_value(old_value, depth + 1)}",
        f"{indent}  + {key}: {format_value(new_value, depth + 1)}"
    ]


def format_nested(indent, key, children, depth):
    """
        Formats a node representing a nested property in the stylish format.

        Args:
            indent (str): The current indentation string.
            key (str): The key of the nested property.
            children (list): The child nodes of the nested property.
            depth (int): The current depth level in the nested structure.

        Returns:
            list: The list of formatted strings with the nested property.
        """
    result = [f"{indent}    {key}: {{"]
    result.append(stylish(children, depth + 1))
    result.append(f"{indent}    }}")
    return result


def stylish(diff, depth=0):
    """
    Formats the difference into a stylish representation.

    Args:
        diff (list): The difference tree, where each node represents a change.
        depth (int, optional): The current depth level in the nested structure.

    Returns:
        str: The string representation of the differences in stylish format.
    """
    indent = "    " * depth
    result = []

    node_handlers = {
        'added': lambda node: [
            format_added(
                indent,
                node['key'],
                node['value'],
                depth
            )
        ],
        'removed': lambda node: [
            format_removed(
                indent,
                node['key'],
                node['value'],
                depth
            )
        ],
        'unchanged': lambda node: [
            format_unchanged(
                indent,
                node['key'],
                node['value'],
                depth
            )
        ],
        'updated': lambda node: format_updated(
            indent,
            node['key'],
            node['old_value'],
            node['new_value'],
            depth
        ),
        'nested': lambda node: format_nested(
            indent,
            node['key'],
            node['children'],
            depth
        ),
    }

    for node in diff:
        handler = node_handlers.get(node['type'])
        if handler:
            result.extend(handler(node))

    if depth == 0:
        return "{\n" + "\n".join(result) + "\n}"
    return "\n".join(result)
