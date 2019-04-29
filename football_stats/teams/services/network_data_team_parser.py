
from typing import List, Dict, Any, Generator
from teams.models import Team


def valid_team(team: Dict[Any, Any]) -> bool:
    return team['TeamId'] and team['TeamName']


def clean_teams(teams: List[Dict[Any, Any]]) -> Generator:
    return (team for team in teams if valid_team(team))


def insert_into_database(teams: List[Dict[Any, Any]]) -> Dict[int, Team]:
    all_teams = clean_teams(teams)
    all_teams = (
        Team(external_id=team['TeamId'],
             team_name=team['TeamName'],
             team_icon_url=team['TeamIconUrl']
             )
        for team in all_teams)
    created_teams = Team.objects.bulk_create(all_teams)
    return {team.external_id: team for team in created_teams}
