from dataclasses import dataclass
from matches.models import Match, Goal
from typing import List
from django.utils import timezone


@dataclass
class MatchInfo:
    match: Match
    goals_team_1: List[Goal]
    goals_team_2: List[Goal]

    @property
    def score(self) -> str:
        if timezone.now() > self.match.match_time_utc:
            return "{} - {}".format(
                len(self.goals_team_1),
                len(self.goals_team_2),
            )
        return "? - ?"
