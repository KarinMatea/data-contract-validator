import pytest

from data_contract_validator.providers import (
    MockTennisLiveProvider,
    TennisApiProvider,
    map_api_tennis_to_contract,
    map_the_odds_event_to_contract,
    map_to_tennis_match_contract,
    normalize_api_tennis_match,
    normalize_raw_match,
    normalize_the_odds_event,
    validate_api_tennis_matches,
    validate_live_tennis_matches,
    validate_the_odds_events,
)


def test_mock_provider_returns_matches():
    provider = MockTennisLiveProvider()

    matches = provider.fetch_live_matches()

    assert isinstance(matches, list)
    assert len(matches) == 2
    assert matches[0]["event_name"] == "Wimbledon"


def test_normalize_raw_match_supports_alternative_field_names():
    raw_match = {
        "tournament": "Wimbledon",
        "surface": "Grass",
        "round": "F",
        "best_of": 5,
        "player1": "Carlos Alcaraz",
        "player2": "Novak Djokovic",
        "winner": "Carlos Alcaraz",
        "score": "1-6 7-6(6) 6-1 3-6 6-4",
    }

    normalized_match = normalize_raw_match(raw_match)

    assert normalized_match["tournament_name"] == "Wimbledon"
    assert normalized_match["player_1"] == "Carlos Alcaraz"
    assert normalized_match["player_2"] == "Novak Djokovic"


def test_normalize_api_tennis_match_maps_provider_fields():
    raw_match = {
        "event_first_player": "C. Chidekh",
        "event_second_player": "M. Cassone",
        "event_winner": "First Player",
        "event_final_result": "2 - 0",
        "tournament_name": "ITF M25 Wichita, KS Men",
        "tournament_round": "SF",
    }

    normalized_match = normalize_api_tennis_match(raw_match)

    assert normalized_match["player_1"] == "C. Chidekh"
    assert normalized_match["player_2"] == "M. Cassone"
    assert normalized_match["winner"] == "C. Chidekh"
    assert normalized_match["round"] == "SF"


def test_normalize_the_odds_event_maps_provider_fields():
    raw_event = {
        "id": "event-1",
        "sport_key": "tennis_atp_french_open",
        "sport_title": "ATP French Open",
        "commence_time": "2025-05-31T09:00:00Z",
        "home_team": "Tallon Griekspoor",
        "away_team": "Ethan Quinn",
        "bookmakers": [
            {"markets": [{"key": "h2h"}, {"key": "spreads"}]},
            {"markets": [{"key": "h2h"}]},
        ],
    }

    normalized_event = normalize_the_odds_event(raw_event)

    assert normalized_event["event_id"] == "event-1"
    assert normalized_event["bookmaker_count"] == 2
    assert normalized_event["market_count"] == 3


def test_map_to_tennis_match_contract_returns_valid_model():
    raw_match = {
        "event_name": "Wimbledon",
        "court_surface": "Grass",
        "match_round": "F",
        "format_best_of": 5,
        "home_player": "Carlos Alcaraz",
        "away_player": "Novak Djokovic",
        "match_winner": "Carlos Alcaraz",
        "final_score": "1-6 7-6(6) 6-1 3-6 6-4",
    }

    match = map_to_tennis_match_contract(raw_match)

    assert match.tournament_name == "Wimbledon"
    assert match.surface == "Grass"
    assert match.winner == "Carlos Alcaraz"


def test_map_api_tennis_to_contract_returns_model():
    raw_match = {
        "event_first_player": "C. Chidekh",
        "event_second_player": "M. Cassone",
        "event_winner": "First Player",
        "event_final_result": "2 - 0",
        "tournament_name": "ITF M25 Wichita, KS Men",
        "tournament_round": "SF",
    }

    match = map_api_tennis_to_contract(raw_match)

    assert match.tournament_name == "ITF M25 Wichita, KS Men"
    assert match.player_1 == "C. Chidekh"
    assert match.winner == "C. Chidekh"


def test_map_the_odds_event_to_contract_returns_model():
    raw_event = {
        "id": "event-1",
        "sport_key": "tennis_atp_french_open",
        "sport_title": "ATP French Open",
        "commence_time": "2025-05-31T09:00:00Z",
        "home_team": "Tallon Griekspoor",
        "away_team": "Ethan Quinn",
        "bookmakers": [
            {"markets": [{"key": "h2h"}]},
        ],
    }

    event = map_the_odds_event_to_contract(raw_event)

    assert event.event_id == "event-1"
    assert event.home_team == "Tallon Griekspoor"
    assert event.bookmaker_count == 1


def test_validate_live_tennis_matches_splits_valid_and_invalid_matches():
    provider = MockTennisLiveProvider()

    raw_matches = provider.fetch_live_matches()
    valid_matches, errors = validate_live_tennis_matches(raw_matches)

    assert len(valid_matches) == 1
    assert len(errors) == 1
    assert errors[0]["record_number"] == 2


def test_validate_api_tennis_matches_returns_results():
    raw_matches = [
        {
            "event_first_player": "C. Chidekh",
            "event_second_player": "M. Cassone",
            "event_winner": "First Player",
            "event_final_result": "2 - 0",
            "tournament_name": "ITF M25 Wichita, KS Men",
            "tournament_round": "SF",
        }
    ]

    valid_matches, errors = validate_api_tennis_matches(raw_matches)

    assert len(valid_matches) == 1
    assert len(errors) == 0


def test_validate_the_odds_events_returns_results():
    raw_events = [
        {
            "id": "event-1",
            "sport_key": "tennis_atp_french_open",
            "sport_title": "ATP French Open",
            "commence_time": "2025-05-31T09:00:00Z",
            "home_team": "Tallon Griekspoor",
            "away_team": "Ethan Quinn",
            "bookmakers": [
                {"markets": [{"key": "h2h"}]},
            ],
        }
    ]

    valid_events, errors = validate_the_odds_events(raw_events)

    assert len(valid_events) == 1
    assert len(errors) == 0


def test_tennis_api_provider_raises_for_missing_api_key(monkeypatch):
    monkeypatch.delenv("TENNIS_API_KEY", raising=False)
    monkeypatch.setenv("TENNIS_API_BASE_URL", "https://example.com/live")

    provider = TennisApiProvider()

    with pytest.raises(ValueError, match="Missing API key"):
        provider.fetch_live_matches()
        
def test_normalize_api_tennis_match_maps_semifinals_text():
    raw_match = {
        "event_first_player": "Player A",
        "event_second_player": "Player B",
        "event_winner": "First Player",
        "event_final_result": "2 - 0",
        "tournament_name": "Sample Event",
        "tournament_round": "Semi-finals",
    }

    normalized_match = normalize_api_tennis_match(raw_match)

    assert normalized_match["round"] == "SF"