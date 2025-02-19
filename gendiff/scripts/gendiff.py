from gendiff.gendiff import generate_diff
from gendiff.parser_args import parse_args


def main():
    args = parse_args()
    result = generate_diff(
        args.first_file,
        args.second_file,
        format_type=args.format
    )
    print(result)


if __name__ == '__main__':
    main()
