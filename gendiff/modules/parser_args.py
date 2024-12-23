import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file', help='path to the first file')
    parser.add_argument('second_file', help='path to the first file')
    parser.add_argument('-f', '--format',
                        choices=['stylish'],
                        default='stylish',
                        help='set format of output (default: stylish)')
    return parser.parse_args(args)
