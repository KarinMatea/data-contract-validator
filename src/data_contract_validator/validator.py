import csv
import json
from pathlib import Path

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


def validate_users(data: list[dict]) -> tuple[list[UserContract], list[dict]]:
    valid_users = []
    errors = []

    for index, item in enumerate(data):
        try:
            user = UserContract.model_validate(item)
            valid_users.append(user)
        except ValidationError as exc:
            errors.append(
                {
                    "index": index,
                    "input": item,
                    "errors": exc.errors(),
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
            lines.append(f"- Record index {error['index']}")

            for detail in error["errors"]:
                field_path = ".".join(str(part) for part in detail["loc"])
                message = detail["msg"]
                lines.append(f"  - Field '{field_path}': {message}")

    return "\n".join(lines)