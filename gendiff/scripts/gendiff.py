from gendiff.modules.gendiff import generate_diff
from gendiff.modules.parser_args import parse_args


def main():
    args = parse_args()
    result = generate_diff(args.first_file, args.second_file)
    print(result)


if __name__ == '__main__':
    main()
