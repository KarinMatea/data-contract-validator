from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserContract(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=18)


class Surface(StrEnum):
    HARD = "Hard"
    CLAY = "Clay"
    GRASS = "Grass"


class Round(StrEnum):
    R128 = "R128"
    R64 = "R64"
    R32 = "R32"
    R16 = "R16"
    QF = "QF"
    SF = "SF"
    F = "F"


class TennisMatchContract(BaseModel):
    tournament_name: str = Field(min_length=1)
    surface: Surface
    round: Round
    best_of: int = Field(ge=3, le=5)
    player_1: str = Field(min_length=1)
    player_2: str = Field(min_length=1)
    winner: str = Field(min_length=1)
    score: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_match_rules(self):
        if self.player_1 == self.player_2:
            raise ValueError("player_1 and player_2 must be different players")

        if self.winner not in {self.player_1, self.player_2}:
            raise ValueError("winner must match player_1 or player_2")

        return self


class TennisOddsEventContract(BaseModel):
    event_id: str = Field(min_length=1)
    sport_key: str = Field(min_length=1)
    sport_title: str = Field(min_length=1)
    commence_time: str = Field(min_length=1)
    home_team: str = Field(min_length=1)
    away_team: str = Field(min_length=1)
    bookmaker_count: int = Field(ge=0)
    market_count: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_event_rules(self):
        if self.home_team == self.away_team:
            raise ValueError("home_team and away_team must be different")

        return self