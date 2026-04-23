import pytest
from pydantic import ValidationError

from data_contract_validator.models import TennisMatchContract


def test_valid_tennis_match_contract():
    match = TennisMatchContract(
        tournament_name="Wimbledon",
        surface="Grass",
        round="F",
        best_of=5,
        player_1="Carlos Alcaraz",
        player_2="Novak Djokovic",
        winner="Carlos Alcaraz",
        score="1-6 7-6(6) 6-1 3-6 6-4",
    )

    assert match.tournament_name == "Wimbledon"
    assert match.surface == "Grass"
    assert match.round == "F"
    assert match.winner == "Carlos Alcaraz"


def test_winner_must_match_one_of_the_players():
    with pytest.raises(ValidationError, match="winner must match player_1 or player_2"):
        TennisMatchContract(
            tournament_name="Australian Open",
            surface="Hard",
            round="SF",
            best_of=5,
            player_1="Jannik Sinner",
            player_2="Daniil Medvedev",
            winner="Roger Federer",
            score="6-3 6-3 6-3",
        )


def test_players_must_be_different():
    with pytest.raises(ValidationError, match="player_1 and player_2 must be different players"):
        TennisMatchContract(
            tournament_name="US Open",
            surface="Hard",
            round="QF",
            best_of=5,
            player_1="Novak Djokovic",
            player_2="Novak Djokovic",
            winner="Novak Djokovic",
            score="6-4 6-4 6-4",
        )