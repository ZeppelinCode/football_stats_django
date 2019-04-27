from typing import List, Dict, Any, Optional
from matches.models import (Match, Location, Goal,
                            Outcome, MatchDayMetadata)
from teams.models import Team
from itertools import groupby
from pytz import timezone
from datetime import datetime


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

    # TODO handle time formats, last_update is not utc..
    return Match(
        external_id=raw_match['MatchID'],
        match_time_utc=raw_match['MatchDateTimeUTC'],
        league_name=raw_match['LeagueName'],
        location=match_location,
        matchday=raw_match['Group']['GroupOrderID'],
        viewers=raw_match['NumberOfViewers'],
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
    all_goals = []
    all_outcomes = []
    for raw_match in raw_matches:

        raw_goals = raw_match['Goals']
        team1 = raw_team_to_model_team[raw_match['Team1']['TeamId']]
        team2 = raw_team_to_model_team[raw_match['Team2']['TeamId']]
        match = raw_matches_to_model_matches[raw_match['MatchID']]

        score_team1 = 0
        score_team2 = 0
        for raw_goal in raw_goals:
            scoring_team = None
            new_score_team1 = raw_goal['ScoreTeam1']
            new_score_team2 = raw_goal['ScoreTeam2']
            if new_score_team1 > score_team1:
                scoring_team = team1
                score_team1 = new_score_team1
            else:
                scoring_team = team2
                score_team2 = new_score_team2

            goal = Goal(
                external_id=raw_goal['GoalID'],
                goal_getter_name=raw_goal['GoalGetterName'],
                match=match,
                match_minute=raw_goal['MatchMinute'],
                team=scoring_team)
            all_goals.append(goal)

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

    Goal.objects.bulk_create(all_goals)
    Outcome.objects.bulk_create(all_outcomes)


def insert_matchday_info(
    current_group,
    last_change: str
):
    matchday = current_group['GroupOrderID']
    MatchDayMetadata.objects.create(
        matchday=matchday,
        last_update=western_europe_time_to_utc(last_change)
    )


def western_europe_time_to_utc(dt: Optional[str]):
    if dt is None:
        return dt

    datetime_obj = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f")
    datetime_obj_as_western_europe_time = datetime_obj.replace(
        tzinfo=timezone('Europe/Berlin'))
    return datetime_obj_as_western_europe_time.astimezone(
        timezone('UTC'))
