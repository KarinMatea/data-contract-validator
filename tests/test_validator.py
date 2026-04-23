import pytest

from data_contract_validator.validator import (
    build_validation_report,
    load_csv_file,
    load_data_file,
    load_json_file,
    validate_users,
)


def test_load_json_file_returns_list():
    data = load_json_file("sample_data/users.json")

    assert isinstance(data, list)
    assert len(data) == 3


def test_load_csv_file_returns_list():
    data = load_csv_file("sample_data/users.csv")

    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["name"] == "Anna"


def test_validate_users_splits_valid_and_invalid_records_for_json():
    data = load_json_file("sample_data/users.json")

    valid_users, errors = validate_users(data)

    assert len(valid_users) == 2
    assert len(errors) == 1
    assert errors[0]["index"] == 2
    assert errors[0]["record_number"] == 3


def test_validate_users_splits_valid_and_invalid_records_for_csv():
    data = load_csv_file("sample_data/users.csv")

    valid_users, errors = validate_users(data)

    assert len(valid_users) == 2
    assert len(errors) == 1
    assert errors[0]["record_number"] == 3


def test_validation_error_contains_field_details():
    data = load_json_file("sample_data/users.json")

    _, errors = validate_users(data)

    first_error = errors[0]["errors"][0]

    assert "field" in first_error
    assert "message" in first_error
    assert "error_type" in first_error
    assert "input_value" in first_error


def test_build_validation_report_contains_record_and_value():
    data = load_json_file("sample_data/users.json")
    valid_users, errors = validate_users(data)

    report = build_validation_report(valid_users, errors)

    assert "Validation Report" in report
    assert "Record 3" in report
    assert "Field 'email'" in report
    assert "value='invalid-email'" in report


def test_load_json_file_raises_for_non_list_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"id": 1, "name": "Anna"}', encoding="utf-8")

    with pytest.raises(ValueError, match="JSON file must contain a list of objects"):
        load_json_file(str(file_path))


def test_load_data_file_raises_for_unsupported_extension(tmp_path):
    file_path = tmp_path / "users.txt"
    file_path.write_text("some text", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_data_file(str(file_path))