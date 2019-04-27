from matches.models import (Outcome, MatchDayMetadata)
from django.db.models import Count
from teams.services.domain import (
    TeamRepresentation, init_team, TeamsStatsName, TeamStatsId)
from django.core.cache import cache
from typing import List


# Public API
def get_leaderboard() -> List[TeamRepresentation]:
    """
    Returns a sorted list of all teams by points.
    """
    return get_cached_value('leaderboard')


def get_teams_by_name_similarity(name: str) -> List[TeamRepresentation]:
    team_stats = get_cached_value('team_stats_name')
    similar = {team_name: team_representation
               for team_name, team_representation
               in team_stats.items()
               if name in team_name}
    return calculate_leaderboard(similar)


def get_team(team_id: int) -> TeamRepresentation:
    team_stats = get_cached_value('team_stats_id')
    return team_stats[team_id]


# Private helpers
def get_cached_value(key: str):
    value = cache.get(key)
    if value is None:
        cache_contents = reaload_cache()
        return cache_contents[key]

    return value


def reaload_cache() -> dict:
    team_stats_name = build_team_stats_name(get_all_outcomes())
    leaderboard = calculate_leaderboard(team_stats_name)
    add_rank_to_team_stats(leaderboard)
    team_stats_id = build_team_stats_id(team_stats_name)
    cache_contents = {
        'team_stats_name': team_stats_name,
        'team_stats_id': team_stats_id,
        'leaderboard': leaderboard,
        'current_matchday': get_matchday_metadata()
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


def build_team_stats_name(outcomes) -> TeamsStatsName:
    """
    Builds structured classes out of a database aggregate and stores them
    in a team_name -> TeamRepresentation dictionary.
    """
    team_performances: TeamsStatsName = {}
    for outcome in outcomes:
        team_name = outcome['team__team_name']
        team_performance = team_performances.get(
            team_name, init_team(outcome['team_id'], team_name))
        setattr(team_performance,
                outcome['outcome_type'], outcome['outcome_type_count'])
        team_performances[team_name] = team_performance

    calculate_and_add_points(team_performances)

    return team_performances


def build_team_stats_id(stats: TeamsStatsName) -> TeamStatsId:
    """
    Builds a team_id -> TeamRepresentation dictionary from a
    team_name -> TeamRepresentation dictionary.
    """
    id_to_representation_dict = {}
    for team_representation in stats.values():
        id_to_representation_dict[team_representation.id] = team_representation
    return id_to_representation_dict


def calculate_leaderboard(
    teams_stats: TeamsStatsName
) -> List[TeamRepresentation]:
    """
    Sorts teams by points.
    """
    return sorted(
        teams_stats.values(),
        key=lambda tp: tp.points,
        reverse=True)


def calculate_and_add_points(team_performances: TeamsStatsName):
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


def get_matchday_metadata():
    return MatchDayMetadata.objects.order_by('-matchday')[0]


reaload_cache()
