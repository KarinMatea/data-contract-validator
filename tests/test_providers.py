from data_contract_validator.providers import (
    MockTennisLiveProvider,
    map_to_tennis_match_contract,
    validate_live_tennis_matches,
)


def test_mock_provider_returns_matches():
    provider = MockTennisLiveProvider()

    matches = provider.fetch_live_matches()

    assert isinstance(matches, list)
    assert len(matches) == 2
    assert matches[0]["event_name"] == "Wimbledon"


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


def test_validate_live_tennis_matches_splits_valid_and_invalid_matches():
    provider = MockTennisLiveProvider()

    raw_matches = provider.fetch_live_matches()
    valid_matches, errors = validate_live_tennis_matches(raw_matches)

    assert len(valid_matches) == 1
    assert len(errors) == 1
    assert errors[0]["record_number"] == 2