from matches.models import (Outcome, MatchDayMetadata)
from django.db.models import Count
from teams.services.domain import (
    TeamRepresentation, init_team, NameToTeamStats, IdToTeamStats)
from django.core.cache import cache
from typing import List

NAME_TO_TEAM_STATS = 'name_to_team_stats'
ID_TO_TEAM_STATS = 'id_to_team_stats'
LEADERBOARD = 'leaderboard'
CURRENT_MATCHDAY = 'current_matchday'

# ---------------- Public API ----------------


def get_leaderboard() -> List[TeamRepresentation]:
    """
    Returns a sorted list of all teams by points.
    """
    return get_cached_value('leaderboard')


def get_teams_by_name_similarity(name: str) -> List[TeamRepresentation]:
    team_stats = get_cached_value('name_to_team_stats')
    similar = {team_name: team_representation
               for team_name, team_representation
               in team_stats.items()
               if name in team_name}
    return calculate_leaderboard(similar)


def get_team(team_id: int) -> TeamRepresentation:
    team_stats = get_cached_value('id_to_team_stats')
    return team_stats[team_id]


# ---------------- Private Helpers ----------------
def get_cached_value(key: str):
    value = cache.get(key)
    if value is None:
        cache_contents = reload_cache()
        return cache_contents[key]

    return value


def reload_cache() -> dict:
    name_to_team_stats = build_name_to_team_stats(get_all_outcomes())
    leaderboard = calculate_leaderboard(name_to_team_stats)
    add_rank_to_team_stats(leaderboard)
    id_to_team_stats = build_id_to_team_stats(name_to_team_stats)
    cache_contents = {
        NAME_TO_TEAM_STATS: name_to_team_stats,
        ID_TO_TEAM_STATS: id_to_team_stats,
        LEADERBOARD: leaderboard,
        CURRENT_MATCHDAY: get_matchday_metadata()
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


def build_name_to_team_stats(outcomes) -> NameToTeamStats:
    """
    Builds structured classes out of a database aggregate and stores them
    in a team_name -> TeamRepresentation dictionary.
    """
    team_performances: NameToTeamStats = {}
    for outcome in outcomes:
        team_name = outcome['team__team_name']
        team_performance = team_performances.get(
            team_name, init_team(outcome['team_id'], team_name))
        setattr(team_performance,
                outcome['outcome_type'], outcome['outcome_type_count'])
        team_performances[team_name] = team_performance

    calculate_and_add_points(team_performances)

    return team_performances


def build_id_to_team_stats(stats: NameToTeamStats) -> IdToTeamStats:
    """
    Builds a team_id -> TeamRepresentation dictionary from a
    team_name -> TeamRepresentation dictionary.
    """
    id_to_representation_dict = {}
    for team_representation in stats.values():
        id_to_representation_dict[team_representation.id] = team_representation
    return id_to_representation_dict


def calculate_leaderboard(
    teams_stats: NameToTeamStats
) -> List[TeamRepresentation]:
    """
    Sorts teams by points.
    """
    return sorted(
        teams_stats.values(),
        key=lambda tp: tp.points,
        reverse=True)


def calculate_and_add_points(team_performances: NameToTeamStats):
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
