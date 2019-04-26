from dataclasses import dataclass
from typing import Dict


@dataclass
class TeamRepresentation:
    id: int
    team_name: str
    rank: int
    win: int
    loss: int
    draw: int
    points: int


def init_team(id: int, team_name: str) -> TeamRepresentation:
    return TeamRepresentation(
        id,
        team_name,
        0,
        0,
        0,
        0,
        0
    )


TeamsStatsName = Dict[str, TeamRepresentation]
TeamStatsId = Dict[int, TeamRepresentation]
