from matches.models import Match, Goal, Location
from django.db.models import Q
from matches.services.domain import MatchInfo
from typing import List, Dict


def get_all_matches_for_team(team_id: int) -> List[MatchInfo]:
    all_matches = Match.objects \
        .select_related('location') \
        .filter(Q(team_1__id=team_id) | Q(team_2__id=team_id)) \
        .select_related('team_1') \
        .select_related('team_2')

    matches = {match.id: MatchInfo(
        match=match,
        goals_team_1=[],
        goals_team_2=[])
        for match in all_matches}

    goals = Goal.objects.filter(match_id__in=matches.keys())
    for goal in goals:
        match_info = matches[goal.match_id]
        if match_info is None:
            continue

        if goal.team_id == match_info.match.team_1_id:
            match_info.goals_team_1.append(goal)
        else:
            match_info.goals_team_2.append(goal)

    return sorted(
        matches.values(),
        key=lambda match_info: match_info.match.match_time_utc)