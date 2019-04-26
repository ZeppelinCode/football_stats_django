from dataclasses import dataclass
from matches.models import Match, Location, Goal
from teams.models import Team
from typing import List
from django.core.paginator import Paginator


@dataclass
class MatchInfo:
    match: Match
    goals_team_1: List[Goal]
    goals_team_2: List[Goal]
