import pytest

from data_contract_validator.validator import load_json_file, validate_users


def test_load_json_file_returns_list():
    data = load_json_file("sample_data/users.json")

    assert isinstance(data, list)
    assert len(data) == 3


def test_validate_users_splits_valid_and_invalid_records():
    data = load_json_file("sample_data/users.json")

    valid_users, errors = validate_users(data)

    assert len(valid_users) == 2
    assert len(errors) == 1
    assert errors[0]["index"] == 2


def test_load_json_file_raises_for_non_list_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"id": 1, "name": "Anna"}', encoding="utf-8")

    with pytest.raises(ValueError, match="JSON file must contain a list of objects"):
        load_json_file(str(file_path))