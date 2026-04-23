# Data Contract Validator

Ein Lernprojekt, das CSV- und JSON-Daten gegen definierte Python-Modelle validiert.

## Features

- Validierung von JSON-Dateien
- Validierung von CSV-Dateien
- Fehlerreport im Terminal
- Automatische Tests mit pytest
- CI mit GitHub Actions

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Tests

```bash
ruff check .
pytest
```

## Beispiel

```bash
python -m data_contract_validator sample_data/users.json
python -m data_contract_validator sample_data/users.csv
```