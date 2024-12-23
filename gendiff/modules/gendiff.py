import json
import yaml
from gendiff.modules.parser import load_data


def format_value(value, depth):
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


def generate_diff(file1, file2, format_type="stylish"):
    data1 = load_data(file1)
    data2 = load_data(file2)
    diff = build_diff(data1, data2)

    if format_type == "stylish":
        return stylish(diff)
    elif format_type == "yaml":
        return yaml.dump(diff, sort_keys=False, default_flow_style=False)
    elif format_type == "json":
        return json.dumps(diff, indent=4)
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


def stylish(diff, depth=0):
    indent = "    " * depth
    result = []

    for node in diff:
        key = node['key']
        node_type = node['type']

        if node_type == 'added':
            result.append(
                f"{indent}  + {key}: {format_value(node['value'], depth + 1)}"
            )
        elif node_type == 'removed':
            result.append(
                f"{indent}  - {key}: {format_value(node['value'], depth + 1)}"
            )
        elif node_type == 'unchanged':
            result.append(
                f"{indent}    {key}: {format_value(node['value'], depth + 1)}"
            )
        elif node_type == 'updated':
            result.append(
                f"{indent}  - {key}: "
                f"{format_value(node['old_value'], depth + 1)}"
            )
            result.append(
                f"{indent}  + {key}: "
                f"{format_value(node['new_value'], depth + 1)}"
            )
        elif node_type == 'nested':
            result.append(f"{indent}    {key}: {{")
            result.append(stylish(node['children'], depth + 1))
            result.append(f"{indent}    }}")

    if depth == 0:
        return "{\n" + "\n".join(result) + "\n}"
    else:
        return "\n".join(result)
