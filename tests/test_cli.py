import sys

from data_contract_validator.cli import main


def test_cli_returns_1_for_invalid_json_data(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["data-contract-validator", "sample_data/users.json"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Validation Report" in captured.out
    assert "Valid records: 2" in captured.out
    assert "Invalid records: 1" in captured.out


def test_cli_returns_1_for_invalid_csv_data(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["data-contract-validator", "sample_data/users.csv"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Validation Report" in captured.out
    assert "Valid records: 2" in captured.out
    assert "Invalid records: 1" in captured.out


def test_cli_returns_2_for_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["data-contract-validator", "sample_data/missing.json"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "file not found" in captured.out.lower()