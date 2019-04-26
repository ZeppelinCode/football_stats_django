from matches.models import Match, Goal, Location
from django.db.models import Q
from matches.services.domain import MatchInfo
from typing import List, Dict


def get_all_matches_for_team(team_id: int) -> List[MatchInfo]:
    all_goals = Goal.objects \
        .select_related('match') \
        .filter(Q(match__team_1=team_id) | Q(match__team_2=team_id)) \
        .select_related('team') \
        .select_related('match__location')

    matches: Dict[int, MatchInfo] = {}
    for goal in all_goals:
        match_info = matches.get(
            goal.match_id,
            MatchInfo(
                match=goal.match,
                goals_team_1=[],
                goals_team_2=[]
            ))
        if goal.team_id == match_info.match.team_1_id:
            match_info.goals_team_1.append(goal)
        else:
            match_info.goals_team_2.append(goal)
        matches[goal.match_id] = match_info

    return sorted(
        matches.values(),
        key=lambda match_info: match_info.match.match_time_utc)
