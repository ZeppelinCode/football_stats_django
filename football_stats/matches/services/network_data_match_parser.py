from typing import List, Dict, Any, Tuple
from matches.models import (Match, Location, Goal,
                            Outcome)
from teams.models import Team
from itertools import groupby
from util.util import western_europe_time_to_utc


def extract_locations(
    matches: List[Dict[Any, Any]]
):
    raw_locations = (match['Location']
                     for match in matches if match['Location'])
    locations: Dict[Any, Any] = {}
    for location_id, location in groupby(raw_locations,
                                         key=lambda l: l['LocationID']):
        if location_id in locations:
            continue
        locations[location_id] = next(location)
    return list(locations.values())


def raw_location_to_location_model(location: Dict[Any, Any]) -> Location:
    return Location(
        external_id=location['LocationID'],
        city=location['LocationCity'],
        stadium=location['LocationStadium']
    )


def insert_locations_into_database(
    raw_matches: List[Dict[Any, Any]]
) -> Dict[int, Location]:
    locations = [raw_location_to_location_model(location)
                 for location in extract_locations(raw_matches)]
    created_locations = Location.objects.bulk_create(locations)
    return {location.external_id: location for location in created_locations}


def raw_match_to_match_model(
        raw_match: Dict[Any, Any],
        raw_location_to_model_location: Dict[int, Location],
        raw_team_to_model_team: Dict[int, Team],
) -> Match:
    match_location = None
    if raw_match['Location']:
        external_location_id = raw_match['Location']['LocationID']
        match_location = raw_location_to_model_location[external_location_id]

    team1 = raw_team_to_model_team[raw_match['Team1']['TeamId']]
    team2 = raw_team_to_model_team[raw_match['Team2']['TeamId']]

    return Match(
        external_id=raw_match['MatchID'],
        match_time_utc=raw_match['MatchDateTimeUTC'],
        location=match_location,
        matchday=raw_match['Group']['GroupOrderID'],
        last_update_utc=western_europe_time_to_utc(
            raw_match['LastUpdateDateTime']),
        finished=raw_match['MatchIsFinished'],
        team_1=team1,
        team_2=team2)


def insert_matches_into_database(
        raw_matches: List[Dict[Any, Any]],
        raw_location_to_model_location: Dict[int, Location],
        raw_team_to_model_team: Dict[int, Team],
) -> Dict[int, Match]:
    matches = (raw_match_to_match_model(
        raw_match, raw_location_to_model_location, raw_team_to_model_team)
        for raw_match in raw_matches)
    created_matches = Match.objects.bulk_create(matches)
    return {match.external_id: match for match in created_matches}


def insert_goals_into_database(
    raw_matches: List[Dict[Any, Any]],
    raw_matches_to_model_matches: Dict[int, Match],
    raw_team_to_model_team: Dict[int, Team],
):
    all_goals: List[Goal] = []
    all_outcomes: List[Outcome] = []
    for raw_match in raw_matches:

        raw_goals = raw_match['Goals']
        team1 = raw_team_to_model_team[raw_match['Team1']['TeamId']]
        team2 = raw_team_to_model_team[raw_match['Team2']['TeamId']]
        match = raw_matches_to_model_matches[raw_match['MatchID']]

        match_goals, score_team_1, score_team_2 = transform_goals(
            raw_goals,
            team1.id,
            team2.id,
            match.id
        )
        match_outcomes = get_outcomes(
            match, team1, team2, score_team_1, score_team_2)

        all_goals += match_goals
        all_outcomes += match_outcomes

    Goal.objects.bulk_create(all_goals)
    Outcome.objects.bulk_create(all_outcomes)


def transform_goals(
    raw_goals,
    internal_team_1_id: int,
    internal_team_2_id: int,
    internal_match_id: int
) -> Tuple[List[Goal], int, int]:
    """
    Converts a list of response goals to a list of Goal models.
    Also calculates the score for each team.
    """
    goals = []
    score_team_1 = 0
    score_team_2 = 0
    for goal in raw_goals:
        team_that_scored = internal_team_2_id
        new_score_team_1 = goal['ScoreTeam1']
        new_score_team_2 = goal['ScoreTeam2']
        if new_score_team_1 > score_team_1:
            team_that_scored = internal_team_1_id
            score_team_1 = new_score_team_1
        else:
            score_team_2 = new_score_team_2
        goals.append(
            Goal(
                external_id=goal['GoalID'],
                goal_getter_name=goal['GoalGetterName'],
                match_id=internal_match_id,
                match_minute=goal['MatchMinute'],
                team_id=team_that_scored
            )
        )

    return goals, score_team_1, score_team_2


def get_outcomes(
        match: Match,
        team1: Team,
        team2: Team,
        score_team1: int,
        score_team2: int
) -> List[Outcome]:
    # Can't have a match outcome if the match is still being played
    if not match.finished:
        return []

    all_outcomes = []
    if score_team1 > score_team2:
        all_outcomes.append(
            Outcome(match=match, team=team1, outcome_type='win'))
        all_outcomes.append(
            Outcome(match=match, team=team2, outcome_type='loss'))
    elif score_team1 < score_team2:
        all_outcomes.append(
            Outcome(match=match, team=team1, outcome_type='loss'))
        all_outcomes.append(
            Outcome(match=match, team=team2, outcome_type='win'))
    else:
        all_outcomes.append(
            Outcome(match=match, team=team1, outcome_type='draw'))
        all_outcomes.append(
            Outcome(match=match, team=team2, outcome_type='draw'))
    return all_outcomes
