# Data Contract Validator

Ein Python-Projekt zum Validieren strukturierter Daten aus JSON-, CSV- und Live-Sportquellen. Das Repository begann als kompakter Data-Contract-Validator für User-Daten und wurde schrittweise zu einem praxisnahen Tennis-Projekt erweitert: mit Domain-Modellen, Provider-Adaptern, CLI, HTML-Report und CI über GitHub Actions.

## Projektüberblick

Das Projekt validiert aktuell drei Arten von Eingaben:

- lokale JSON- und CSV-Dateien mit User-Daten,
- simulierte Live-Tennis-Matchdaten,
- echte Tennis-Odds-Events über externe APIs wie The Odds API.

Der Kern des Projekts ist bewusst in Schichten aufgebaut: CLI, Provider, Validierungslogik, Reports und Pydantic-Modelle sind getrennt. Dieses `src/`-Layout ist sauber, wartbar und gut für Packaging sowie CI geeignet.

## Features

- Validierung von JSON- und CSV-Dateien mit strukturierten Fehlerreports.
- Pydantic-Modelle für User-, Tennis-Match- und Tennis-Odds-Event-Daten.
- Mock-Provider für reproduzierbare lokale Entwicklung und stabile Tests.
- Provider-Schicht für externe APIs mit sauberer Trennung zwischen Fremdformat und internem Domainmodell.
- CLI mit mehreren Modi für Datei-Validierung und Live-Datenabrufe.
- HTML-Report-Ausgabe für validierte Datensätze und Fehlerübersichten.
- Linting, Tests und CI mit GitHub Actions.

## Projektstruktur

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── sample_data/
│   ├── users.json
│   ├── users.csv
│   └── api_tennis_live_sample.json
├── src/
│   └── data_contract_validator/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── models.py
│       ├── providers.py
│       ├── reporting.py
│       └── validator.py
├── tests/
│   ├── test_cli.py
│   ├── test_models.py
│   ├── test_providers.py
│   ├── test_reporting.py
│   ├── test_tennis_models.py
│   └── test_validator.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Installation

### Voraussetzungen

- Python 3.11+
- `pip`
- optional eine virtuelle Umgebung

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Nutzung

### User-Daten aus JSON validieren

```bash
data-contract-validator sample_data/users.json
```

### User-Daten aus CSV validieren

```bash
data-contract-validator sample_data/users.csv
```

### Mock-Tennisdaten validieren

```bash
data-contract-validator --live-tennis
```

### Externe Tennis-API validieren

```bash
data-contract-validator --live-tennis-api
```

### The Odds API für Tennis-Odds-Events nutzen

```bash
data-contract-validator --live-tennis-odds
```

### Optional HTML-Report erzeugen

```bash
data-contract-validator sample_data/users.json --html-report output/report.html
```

## Konfiguration

Lokale Secrets und Laufzeitkonfiguration gehören **nicht** in den Code oder ins Repository, sondern in Umgebungsvariablen oder eine lokale `.env`-Datei.

Beispiel für eine lokale `.env`:

```env
TENNIS_API_KEY=your_api_key_here
TENNIS_API_BASE_URL=https://example.com/api/live-tennis
TENNIS_ODDS_API_KEY=your_the_odds_api_key_here
TENNIS_ODDS_SPORT=upcoming
TENNIS_ODDS_REGIONS=uk
TENNIS_ODDS_MARKETS=h2h
TENNIS_ODDS_FORMAT=decimal
```

## Architektur

### Modelle

Die Domänenmodelle sind mit Pydantic umgesetzt. Aktuell enthalten die Modelle unter anderem:

- `UserContract`
- `TennisMatchContract`
- `TennisOddsEventContract`

### Provider

Provider kapseln externe Datenquellen und übersetzen deren Antwortformate in interne Modelle. Das entspricht dem Adapter-Gedanken: instabile oder fremde Schnittstellen werden an einer Stelle normalisiert, während der Rest des Systems gegen ein stabiles internes Format arbeitet.

Aktuell gibt es:

- `MockTennisLiveProvider`
- `TennisApiProvider`
- `TheOddsApiProvider`

### Reports

Validierungsergebnisse werden sowohl als Konsolenreport als auch optional als HTML-Report ausgegeben. So bleibt das Tool für lokale Nutzung ebenso geeignet wie für vorzeigbare Artefakte im Portfolio.

## Qualitätssicherung

### Linting

```bash
ruff check .
```

### Tests

```bash
pytest
```

Die Tests prüfen Modelle, Provider, CLI und Reports.

### CI mit GitHub Actions

GitHub Actions führt die definierten Workflows in einer frischen Umgebung aus und eignet sich sehr gut für Build-, Lint- und Test-Pipelines in Python-Projekten.

Ein typischer Workflow umfasst:

- Checkout des Repositories,
- Python-Setup,
- Installation der Abhängigkeiten,
- `ruff check .`,
- `pytest`.

## The Odds API Hinweis

The Odds API liefert in erster Linie **Odds- und Event-Daten**, nicht vollständige Punkt-für-Punkt-Tennis-Scoring-Daten. Für dieses Projekt wird die API daher als Quelle für validierbare Tennis-Event- und Odds-Strukturen genutzt, etwa mit Feldern wie `sport_key`, `commence_time`, `home_team`, `away_team` und `bookmakers`.

Das ist bewusst als eigener Contract-Typ modelliert, damit Odds-Daten nicht künstlich in ein Match-Scoring-Modell gepresst werden.
