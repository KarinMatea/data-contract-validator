import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

from data_contract_validator.models import TennisMatchContract

load_dotenv()


class MockTennisLiveProvider:
    def fetch_live_matches(self) -> list[dict[str, Any]]:
        return [
            {
                "event_name": "Wimbledon",
                "court_surface": "Grass",
                "match_round": "F",
                "format_best_of": 5,
                "home_player": "Carlos Alcaraz",
                "away_player": "Novak Djokovic",
                "match_winner": "Carlos Alcaraz",
                "final_score": "1-6 7-6(6) 6-1 3-6 6-4",
            },
            {
                "event_name": "Australian Open",
                "court_surface": "Hard",
                "match_round": "SF",
                "format_best_of": 5,
                "home_player": "Jannik Sinner",
                "away_player": "Daniil Medvedev",
                "match_winner": "Roger Federer",
                "final_score": "6-3 6-3 6-3",
            },
        ]


class TennisApiProvider:
    def __init__(
        self,
        base_url: str | None = None,
        api_key_env: str = "TENNIS_API_KEY",
    ) -> None:
        self.base_url = base_url or os.getenv("TENNIS_API_BASE_URL")
        self.api_key = os.getenv(api_key_env)

    def fetch_live_matches(self) -> list[dict[str, Any]]:
        if not self.api_key:
            raise ValueError("Missing API key. Please set TENNIS_API_KEY.")

        if not self.base_url:
            raise ValueError(
                "Missing API base URL. Please set TENNIS_API_BASE_URL."
            )

        response = requests.get(
            self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=10,
        )
        response.raise_for_status()

        payload = response.json()
        return extract_match_list(payload)


def extract_match_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        if "results" in payload and isinstance(payload["results"], list):
            return payload["results"]

        if "matches" in payload and isinstance(payload["matches"], list):
            return payload["matches"]

        if "result" in payload and isinstance(payload["result"], list):
            return payload["result"]

    if isinstance(payload, list):
        return payload

    raise ValueError(
        "Expected API response to be a list of matches "
        "or a dict with 'result', 'results', or 'matches'"
    )


def load_sample_api_payload(file_path: str) -> list[dict[str, Any]]:
    with open(file_path, encoding="utf-8") as file:
        payload = json.load(file)

    return extract_match_list(payload)


def get_first_available_value(
    raw_match: dict[str, Any],
    candidate_keys: list[str],
) -> Any:
    for key in candidate_keys:
        if key in raw_match and raw_match[key] not in (None, ""):
            return raw_match[key]

    raise KeyError(f"Missing required field. Tried keys: {candidate_keys}")


def normalize_raw_match(raw_match: dict[str, Any]) -> dict[str, Any]:
    return {
        "tournament_name": get_first_available_value(
            raw_match,
            [
                "event_name",
                "tournament_name",
                "tournament",
                "competition_name",
            ],
        ),
        "surface": get_first_available_value(
            raw_match,
            ["court_surface", "surface"],
        ),
        "round": get_first_available_value(
            raw_match,
            ["match_round", "round"],
        ),
        "best_of": get_first_available_value(
            raw_match,
            ["format_best_of", "best_of"],
        ),
        "player_1": get_first_available_value(
            raw_match,
            ["home_player", "player_1", "player1", "competitor_1"],
        ),
        "player_2": get_first_available_value(
            raw_match,
            ["away_player", "player_2", "player2", "competitor_2"],
        ),
        "winner": get_first_available_value(
            raw_match,
            ["match_winner", "winner"],
        ),
        "score": get_first_available_value(
            raw_match,
            ["final_score", "score"],
        ),
    }


def normalize_api_tennis_match(raw_match: dict[str, Any]) -> dict[str, Any]:
    winner = raw_match.get("event_winner")
    player_1 = raw_match.get("event_first_player")
    player_2 = raw_match.get("event_second_player")

    if winner == "First Player":
        winner = player_1
    elif winner == "Second Player":
        winner = player_2
    elif winner is None:
        winner = "LIVE_MATCH_IN_PROGRESS"

    tournament_round = raw_match.get("tournament_round", "")
    if tournament_round == "Quarter-finals":
        normalized_round = "QF"
    elif tournament_round == "Semi-finals":
        normalized_round = "SF"
    elif tournament_round == "Final":
        normalized_round = "F"
    else:
        normalized_round = raw_match.get("tournament_round") or "R32"

    return {
        "tournament_name": raw_match["tournament_name"],
        "surface": "Hard",
        "round": normalized_round,
        "best_of": 3,
        "player_1": player_1,
        "player_2": player_2,
        "winner": winner,
        "score": raw_match.get("event_final_result") or "0-0",
    }


def map_to_tennis_match_contract(raw_match: dict[str, Any]) -> TennisMatchContract:
    normalized_match = normalize_raw_match(raw_match)
    return TennisMatchContract(**normalized_match)


def map_api_tennis_to_contract(raw_match: dict[str, Any]) -> TennisMatchContract:
    normalized_match = normalize_api_tennis_match(raw_match)
    return TennisMatchContract(**normalized_match)


def validate_live_tennis_matches(
    raw_matches: list[dict[str, Any]],
) -> tuple[list[TennisMatchContract], list[dict[str, Any]]]:
    valid_matches = []
    errors = []

    for index, raw_match in enumerate(raw_matches):
        try:
            match = map_to_tennis_match_contract(raw_match)
            valid_matches.append(match)
        except Exception as exc:
            errors.append(
                {
                    "index": index,
                    "record_number": index + 1,
                    "input": raw_match,
                    "errors": [
                        {
                            "field": "provider_payload",
                            "message": str(exc),
                            "error_type": exc.__class__.__name__,
                            "input_value": raw_match,
                        }
                    ],
                }
            )

    return valid_matches, errors


def validate_api_tennis_matches(
    raw_matches: list[dict[str, Any]],
) -> tuple[list[TennisMatchContract], list[dict[str, Any]]]:
    valid_matches = []
    errors = []

    for index, raw_match in enumerate(raw_matches):
        try:
            match = map_api_tennis_to_contract(raw_match)
            valid_matches.append(match)
        except Exception as exc:
            errors.append(
                {
                    "index": index,
                    "record_number": index + 1,
                    "input": raw_match,
                    "errors": [
                        {
                            "field": "provider_payload",
                            "message": str(exc),
                            "error_type": exc.__class__.__name__,
                            "input_value": raw_match,
                        }
                    ],
                }
            )

    return valid_matches, errors