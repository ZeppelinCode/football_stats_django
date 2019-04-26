from matches.models import Outcome
from django.db.models import Count
from typing import List, Tuple
from teams.services.domain import TeamRepresentation, init_team, TeamsStats
from django.core.cache import cache


def get_leaderboard() -> List[TeamRepresentation]:
    """
    Returns a sorted list of all teams by points.
    """
    return _get_cached_value('leaderboard')


def get_teams_by_name_similarity(name: str) -> List[TeamRepresentation]:
    team_stats = _get_cached_value('team_stats')
    return [team_representation
            for team_name, team_representation
            in team_stats.items()
            if name in team_name]


def _get_cached_value(key: str):
    value = cache.get(key)
    if value is None:
        cache_contents = _reaload_cache()
        return cache_contents[key]

    return value


def _reaload_cache() -> dict:
    team_stats = build_team_stats(get_all_outcomes())
    leaderboard = calculate_leaderboard(team_stats)
    add_rank_to_team_stats(leaderboard)
    cache_contents = {
        'team_stats': team_stats,
        'leaderboard': leaderboard
    }

    cache.set_many(cache_contents, 300)

    return cache_contents


def get_all_outcomes():
    """
    Returns an aggregate of the wins, losses and draws 
    of each team in the database.
    """
    return Outcome.objects.values(
        'team__team_name',
        'team_id',
        'outcome_type'
    ).annotate(outcome_type_count=Count('outcome_type'))


def build_team_stats(outcomes) -> TeamsStats:
    """
    Builds structured classes out of a database aggregate.
    """
    team_performances: TeamsStats = {}
    for outcome in outcomes:
        team_name = outcome['team__team_name']
        team_performance = team_performances.get(
            team_name, init_team(outcome['team_id'], team_name))
        setattr(team_performance,
                outcome['outcome_type'], outcome['outcome_type_count'])
        team_performances[team_name] = team_performance

    calculate_and_add_points(team_performances)

    return team_performances


def calculate_leaderboard(
    teams_stats: TeamsStats
) -> List[TeamRepresentation]:
    """
    Sorts teams by points.
    """
    return sorted(
        teams_stats.values(),
        key=lambda tp: tp.points,
        reverse=True)


def calculate_and_add_points(team_performances: TeamsStats):
    """
    Mutates each team representation by calculating the
    points based on the number of wins raws the team has.
    """
    for team_name, team_performance in team_performances.items():
        points = team_performance.win * 3 + team_performance.draw
        team_performance.points = points


def add_rank_to_team_stats(leaderboard: List[TeamRepresentation]):
    """
    Mutates each team representation by calculating the
    rank based on the order of the leaderboard.
    """
    for i, team_representation in enumerate(leaderboard):
        team_representation.rank = i + 1


# Warm up the cache at startup..
_reaload_cache()
