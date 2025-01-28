from gendiff.modules.parser import load_data
from gendiff.modules.formatters.plain import format_plain
from gendiff.modules.formatters.stylish import stylish
from gendiff.modules.formatters.json_formatter import format_json


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
    data1 = load_data(file1)
    data2 = load_data(file2)
    diff = build_diff(data1, data2)

    if format_type == "plain":
        return format_plain(diff)
    elif format_type == 'stylish':
        return stylish(diff)
    elif format_type == "json":
        return format_json(diff)
    else:
        raise ValueError(f"Unsupported format: {format_type}")


def build_diff(data1, data2):
    diff = []
    all_keys = sorted(data1.keys() | data2.keys())

    for key in all_keys:
        if key not in data1:
            diff.append({
                "key": key,
                "type": "added",
                "value": data2[key]
            })
        elif key not in data2:
            diff.append({
                "key": key,
                "type": "removed",
                "value": data1[key]
            })
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            diff.append({
                "key": key,
                "type": "nested",
                "children": build_diff(data1[key], data2[key])
            })
        elif data1[key] != data2[key]:
            diff.append({
                "key": key,
                "type": "updated",
                "old_value": data1[key],
                "new_value": data2[key]
            })
        else:
            diff.append({
                "key": key,
                "type": "unchanged",
                "value": data1[key]
            })
    return diff
