from matches.models import Match, Goal
from django.db.models import Q
from matches.services.domain import MatchInfo
from typing import List, Tuple, Optional, Dict
from django.core.paginator import Paginator
from teams.services.team_service import get_cached_value, CURRENT_MATCHDAY

MATCHES_PER_PAGE = 5


def get_all_matches_paginated(
    page: Optional[int]
) -> Tuple[List[MatchInfo], Paginator]:
    all_matches = get_all_matches_from_db()
    return page_matches(all_matches, page)


def get_team_matches_paginated(
    team_id: int,
    page: Optional[int]
) -> Tuple[List[MatchInfo], Paginator]:
    all_matches = get_all_matches_for_team_from_db(team_id)
    return page_matches(all_matches, page)


def get_upcomming_matches() -> List[MatchInfo]:
    current_matchday = get_cached_value(CURRENT_MATCHDAY).matchday
    db_upcomming_matches = list(Match.objects.filter(
        matchday=current_matchday, finished=False))

    # If there are no upcomming matches for this matchday,
    # the matchday hasn't been updated yet...
    # Show the matches for the next matchday
    if len(db_upcomming_matches) == 0:
        db_upcomming_matches = Match.objects.filter(
            matchday=current_matchday+1, finished=False)

    matches = convert_matches_to_match_info(db_upcomming_matches)

    return sorted(
        matches.values(),
        key=lambda match_info: match_info.match.match_time_utc)


def get_all_matches_from_db():
    return Match.objects \
        .select_related('location') \
        .select_related('team_1') \
        .select_related('team_2') \
        .order_by('match_time_utc')


def get_all_matches_for_team_from_db(team_id: int):
    return get_all_matches_from_db() \
        .filter(Q(team_1__id=team_id) | Q(team_2__id=team_id))


def page_matches(
    all_matches_query_set,
    page: Optional[int]
) -> Tuple[List[MatchInfo], Paginator]:

    paginator = Paginator(all_matches_query_set, MATCHES_PER_PAGE)
    paged_matches = paginator.get_page(page)

    matches = convert_matches_to_match_info(paged_matches)

    return sorted(
        matches.values(),
        key=lambda match_info: match_info.match.match_time_utc), paged_matches


def convert_matches_to_match_info(matches) -> Dict[int, MatchInfo]:
    matches = {match.id: MatchInfo(
        match=match,
        goals_team_1=[],
        goals_team_2=[])
        for match in matches}

    goals = Goal.objects.filter(match_id__in=matches.keys())
    for goal in goals:
        match_info = matches[goal.match_id]
        if match_info is None:
            continue

        if goal.team_id == match_info.match.team_1_id:
            match_info.goals_team_1.append(goal)
        else:
            match_info.goals_team_2.append(goal)

    return matches
