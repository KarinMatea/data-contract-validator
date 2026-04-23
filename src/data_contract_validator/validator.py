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