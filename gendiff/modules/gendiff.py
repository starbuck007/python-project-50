from gendiff.modules.parser import load_data


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    return value


def generate_diff(file1, file2):
    file1_data = load_data(file1)
    file2_data = load_data(file2)

    all_keys = sorted(set(file1_data.keys()).union(set(file2_data.keys())))
    diff = []

    for key in all_keys:
        if key in file1_data and key not in file2_data:
            diff.append(f"  - {key}: {format_value(file1_data[key])}")
        elif key not in file1_data and key in file2_data:
            diff.append(f"  + {key}: {format_value(file2_data[key])}")
        elif file1_data[key] != file2_data[key]:
            diff.append(f"  - {key}: {format_value(file1_data[key])}")
            diff.append(f"  + {key}: {format_value(file2_data[key])}")
        else:
            diff.append(f"    {key}: {format_value(file1_data[key])}")

    return '{\n' + '\n'.join(diff) + '\n}'
