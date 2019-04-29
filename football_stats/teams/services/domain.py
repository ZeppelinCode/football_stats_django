from dataclasses import dataclass
from typing import Dict


@dataclass
class TeamRepresentation:
    id: int
    team_name: str
    team_icon_url: str
    rank: int
    win: int
    loss: int
    draw: int
    points: int


def init_team(
    id: int,
    team_name: str,
    team_icon_url: str
) -> TeamRepresentation:
    return TeamRepresentation(
        id,
        team_name,
        team_icon_url,
        0,
        0,
        0,
        0,
        0
    )


NameToTeamStats = Dict[str, TeamRepresentation]
IdToTeamStats = Dict[int, TeamRepresentation]
