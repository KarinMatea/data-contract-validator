import argparse

from data_contract_validator.reporting import generate_html_report, write_html_report
from data_contract_validator.validator import (
    build_validation_report,
    load_data_file,
    validate_users,
)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="data-contract-validator",
        description="Validate JSON or CSV data against the UserContract schema.",
    )
    parser.add_argument(
        "file_path",
        help="Path to the JSON or CSV file containing user records",
    )
    parser.add_argument(
        "--html-report",
        dest="html_report",
        help="Optional path to write an HTML validation report",
    )
    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    try:
        data = load_data_file(args.file_path)
        valid_users, errors = validate_users(data)

        report = build_validation_report(valid_users, errors)
        print(report)

        if args.html_report:
            html_report = generate_html_report(valid_users, errors)
            write_html_report(args.html_report, html_report)
            print(f"\nHTML report written to: {args.html_report}")

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
