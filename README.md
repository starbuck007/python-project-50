# gendiff
### Hexlet tests and linter status:
[![Actions Status](https://github.com/starbuck007/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/starbuck007/python-project-50/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7ebc82c646ae6fa49eb/maintainability)](https://codeclimate.com/github/starbuck007/python-project-50/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c7ebc82c646ae6fa49eb/test_coverage)](https://codeclimate.com/github/starbuck007/python-project-50/test_coverage)
[![Python CI](https://github.com/starbuck007/python-project-50/actions/workflows/pyci.yml/badge.svg)](https://github.com/starbuck007/python-project-50/actions/workflows/pyci.yml)

a command-line utility for comparing two configuration files and displaying their differences. It supports JSON and YAML file formats, providing a convenient way to analyze changes.

### Description
With gendiff, you can compare configuration files and get a visual representation of the differences. This is useful for tracking changes in files.

### Supported Formats
JSON (.json), YAML (.yaml, .yml)

## Installation
Use poetry to install dependencies:
```poetry install```

## Usage
Example usage for JSON:
```gendiff file1.json file2.json```

[![asciicast](https://asciinema.org/a/Fi5hg69spbEdWIMZOHdwYJWFy.svg)](https://asciinema.org/a/Fi5hg69spbEdWIMZOHdwYJWFy)

Example usage for YAML:
```gendiff file1.yaml file2.yaml```


