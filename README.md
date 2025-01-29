# gendiff
### Hexlet tests and linter status:
[![Actions Status](https://github.com/starbuck007/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/starbuck007/python-project-50/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7ebc82c646ae6fa49eb/maintainability)](https://codeclimate.com/github/starbuck007/python-project-50/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c7ebc82c646ae6fa49eb/test_coverage)](https://codeclimate.com/github/starbuck007/python-project-50/test_coverage)
[![Python CI](https://github.com/starbuck007/python-project-50/actions/workflows/pyci.yml/badge.svg)](https://github.com/starbuck007/python-project-50/actions/workflows/pyci.yml)

a command-line utility for comparing two configuration files and displaying their differences. It supports JSON and YAML file formats, providing a convenient way to analyze changes.

### Description
With gendiff, you can compare configuration files and get a visual representation of the differences. This is useful for tracking changes in files.

## Installation
Follow these steps to install and set up the application using the Makefile:

1. Install the necessary dependencies:
    ```bash
    make install
    ```

2. Build the application:
    ```bash
    make build
    ```

3. Install the package:
    ```bash
    make package-install
    ```

## Usage

1. help
```bash
gendiff -h
```

2. command
```bash
gendiff <filepath1> <filepath2> -f <format>
```
Parameters:
`-f`, `--format` (optional): Specifies the output format. 
Possible values:
- `stylish` (default): Outputs a human-readable diff.
- `plain`: Outputs a plain text diff.
- `json`: Outputs a JSON-formatted diff.

[![asciicast](https://asciinema.org/a/700394.svg)](https://asciinema.org/a/700394)

[![asciicast](https://asciinema.org/a/700396.svg)](https://asciinema.org/a/700396)

[![asciicast](https://asciinema.org/a/700398.svg)](https://asciinema.org/a/700398)

[![asciicast](https://asciinema.org/a/700400.svg)](https://asciinema.org/a/700400)


