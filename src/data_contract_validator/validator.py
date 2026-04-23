import csv
import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from data_contract_validator.models import UserContract


def load_json_file(file_path: str) -> list[dict]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of objects")

    return data


def load_csv_file(file_path: str) -> list[dict]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_data_file(file_path: str) -> list[dict]:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        return load_json_file(file_path)

    if suffix == ".csv":
        return load_csv_file(file_path)

    raise ValueError("Unsupported file type. Please provide a .json or .csv file.")


def get_value_by_path(data: dict, path: tuple[Any, ...]) -> Any:
    current = data

    for part in path:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None

    return current


def validate_users(data: list[dict]) -> tuple[list[UserContract], list[dict]]:
    valid_users = []
    errors = []

    for index, item in enumerate(data):
        try:
            user = UserContract.model_validate(item)
            valid_users.append(user)
        except ValidationError as exc:
            formatted_errors = []

            for detail in exc.errors():
                location = tuple(detail["loc"])
                formatted_errors.append(
                    {
                        "field": ".".join(str(part) for part in location),
                        "message": detail["msg"],
                        "error_type": detail["type"],
                        "input_value": get_value_by_path(item, location),
                    }
                )

            errors.append(
                {
                    "index": index,
                    "record_number": index + 1,
                    "input": item,
                    "errors": formatted_errors,
                }
            )

    return valid_users, errors


def build_validation_report(valid_users: list[UserContract], errors: list[dict]) -> str:
    lines = []
    lines.append("Validation Report")
    lines.append("=================")
    lines.append(f"Valid records: {len(valid_users)}")
    lines.append(f"Invalid records: {len(errors)}")

    if errors:
        lines.append("")
        lines.append("Error details:")

        for error in errors:
            lines.append(f"- Record {error['record_number']}")

            for detail in error["errors"]:
                lines.append(
                    f"  - Field '{detail['field']}': {detail['message']} "
                    f"(value={detail['input_value']!r})"
                )

    return "\n".join(lines)