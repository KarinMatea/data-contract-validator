# Data Contract Validator

Ein Lernprojekt, das CSV- und JSON-Daten gegen definierte Python-Modelle validiert.

## Features

- Validierung von JSON-Dateien
- Validierung von CSV-Dateien
- Fehlerreport im Terminal
- Automatische Tests mit pytest
- Linting mit Ruff
- CI mit GitHub Actions
- Installierbare CLI

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI verwenden

```bash
data-contract-validator sample_data/users.json
data-contract-validator sample_data/users.csv
```

## Tests

```bash
ruff check .
pytest
```

## Alternative Ausführung

```bash
python -m data_contract_validator sample_data/users.json
```