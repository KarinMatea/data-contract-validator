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

        if isinstance(payload, dict):
            if "results" in payload and isinstance(payload["results"], list):
                return payload["results"]

            if "matches" in payload and isinstance(payload["matches"], list):
                return payload["matches"]

        if isinstance(payload, list):
            return payload

        raise ValueError(
            "Expected API response to be a list of matches "
            "or a dict with 'results' or 'matches'"
        )


def map_to_tennis_match_contract(raw_match: dict[str, Any]) -> TennisMatchContract:
    return TennisMatchContract(
        tournament_name=raw_match["event_name"],
        surface=raw_match["court_surface"],
        round=raw_match["match_round"],
        best_of=raw_match["format_best_of"],
        player_1=raw_match["home_player"],
        player_2=raw_match["away_player"],
        winner=raw_match["match_winner"],
        score=raw_match["final_score"],
    )


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