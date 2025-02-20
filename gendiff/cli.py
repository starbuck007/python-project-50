"""
Module for parsing command-line arguments for the difference generator.
"""


import argparse


def parse_args(args=None):
    """ Parses command-line arguments for the difference generator."""
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file', help='path to the first file')
    parser.add_argument('second_file', help='path to the first file')
    parser.add_argument('-f', '--format',
                        choices=['stylish', 'plain', 'json'],
                        default='stylish',
                        help='Set format of output: stylish or plain or json'
                        '(default: stylish)')
    return parser.parse_args(args)
