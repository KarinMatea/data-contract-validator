import pytest

from data_contract_validator.providers import (
    MockTennisLiveProvider,
    TennisApiProvider,
    map_to_tennis_match_contract,
    normalize_raw_match,
    validate_live_tennis_matches,
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


def test_map_to_tennis_match_contract_with_alternative_keys():
    raw_match = {
        "tournament_name": "Wimbledon",
        "surface": "Grass",
        "round": "F",
        "best_of": 5,
        "player_1": "Carlos Alcaraz",
        "player_2": "Novak Djokovic",
        "winner": "Carlos Alcaraz",
        "score": "1-6 7-6(6) 6-1 3-6 6-4",
    }

    match = map_to_tennis_match_contract(raw_match)

    assert match.tournament_name == "Wimbledon"
    assert match.player_1 == "Carlos Alcaraz"
    assert match.player_2 == "Novak Djokovic"


def test_validate_live_tennis_matches_splits_valid_and_invalid_matches():
    provider = MockTennisLiveProvider()

    raw_matches = provider.fetch_live_matches()
    valid_matches, errors = validate_live_tennis_matches(raw_matches)

    assert len(valid_matches) == 1
    assert len(errors) == 1
    assert errors[0]["record_number"] == 2


def test_tennis_api_provider_raises_for_missing_api_key(monkeypatch):
    monkeypatch.delenv("TENNIS_API_KEY", raising=False)
    monkeypatch.setenv("TENNIS_API_BASE_URL", "https://example.com/live")

    provider = TennisApiProvider()

    with pytest.raises(ValueError, match="Missing API key"):
        provider.fetch_live_matches()


def test_tennis_api_provider_raises_for_missing_base_url(monkeypatch):
    monkeypatch.setenv("TENNIS_API_KEY", "fake-key")
    monkeypatch.delenv("TENNIS_API_BASE_URL", raising=False)

    provider = TennisApiProvider()

    with pytest.raises(ValueError, match="Missing API base URL"):
        provider.fetch_live_matches()