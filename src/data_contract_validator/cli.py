import argparse

from data_contract_validator.validator import (
    build_validation_report,
    load_json_file,
    validate_users,
)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="data-contract-validator",
        description="Validate JSON data against the UserContract schema.",
    )
    parser.add_argument(
        "file_path",
        help="Path to the JSON file containing a list of user records",
    )
    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        data = load_json_file(args.file_path)
        valid_users, errors = validate_users(data)
        report = build_validation_report(valid_users, errors)
        print(report)

        if errors:
            return 1

        return 0

    except FileNotFoundError:
        print(f"Error: file not found -> {args.file_path}")
        return 2
    except ValueError as exc:
        print(f"Error: {exc}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())