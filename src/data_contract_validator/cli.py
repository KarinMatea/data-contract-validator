import argparse

import requests

from data_contract_validator.providers import (
    MockTennisLiveProvider,
    TennisApiProvider,
    TheOddsApiProvider,
    validate_api_tennis_matches,
    validate_live_tennis_matches,
    validate_the_odds_events,
)
from data_contract_validator.reporting import generate_html_report, write_html_report
from data_contract_validator.validator import (
    build_validation_report,
    load_data_file,
    validate_users,
)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="data-contract-validator",
        description="Validate JSON/CSV data or fetch tennis live data.",
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "file_path",
        nargs="?",
        help="Path to the JSON or CSV file containing user records",
    )
    input_group.add_argument(
        "--live-tennis",
        action="store_true",
        help="Fetch mock live tennis matches and validate them",
    )
    input_group.add_argument(
        "--live-tennis-api",
        action="store_true",
        help="Fetch live tennis matches from a real API and validate them",
    )
    input_group.add_argument(
        "--live-tennis-odds",
        action="store_true",
        help="Fetch live tennis odds events from The Odds API and validate them",
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
        if args.live_tennis:
            provider = MockTennisLiveProvider()
            raw_matches = provider.fetch_live_matches()
            valid_records, errors = validate_live_tennis_matches(raw_matches)
        elif args.live_tennis_api:
            provider = TennisApiProvider()
            raw_matches = provider.fetch_live_matches()
            valid_records, errors = validate_api_tennis_matches(raw_matches)
        elif args.live_tennis_odds:
            provider = TheOddsApiProvider()
            raw_events = provider.fetch_tennis_odds()
            valid_records, errors = validate_the_odds_events(raw_events)
        else:
            data = load_data_file(args.file_path)
            valid_records, errors = validate_users(data)

        report = build_validation_report(valid_records, errors)
        print(report)

        if args.html_report:
            html_report = generate_html_report(valid_records, errors)
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
    except requests.exceptions.RequestException as exc:
        print(f"Error: failed to fetch live data: {exc}")
        return 4


if __name__ == "__main__":
    raise SystemExit(main())