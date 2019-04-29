from teams.services.team_service import get_cached_value
from matches.models import MatchDayMetadata
from matches.providers.match_provider import get_all_info_for_matchday
from background_task import background
from matches.models import Match, Goal, Outcome
from teams.models import Team
from typing import List, Dict
from matches.services.network_data_match_parser import (
    get_outcomes, transform_goals)
from util.util import western_europe_time_to_utc
from teams.services.team_service import reload_cache
from datetime import datetime
from teams.services.team_service import CURRENT_MATCHDAY
from matches.providers.match_provider import pull_current_match_day_metadata
from background_task.models import Task


def flatten(l):
    return [item for sublist in l for item in sublist]


def external_teams_mapping(current_match_data: List[Match]) -> Dict[int, Team]:
    all_teams = ((m.team_1, m.team_2) for m in current_match_data)
    all_teams = flatten(all_teams)
    return {t.external_id: t for t in all_teams}


def external_match_mapping(current_match_data: List[Match]) -> Dict[int, Match]:
    return {m.external_id: m for m in current_match_data}


@background
def update_matches_if_necessary():
    # TODO ideally would like to inject the result of the network
    # call as function parameter but due to the way background arguments
    # are cached in the db we need to make a fresh call here every time
    new_matchday_metadata = pull_current_match_day_metadata()
    new_matchday = new_matchday_metadata.matchday
    new_update_time = new_matchday_metadata.last_update
    current_matchday = get_cached_value(CURRENT_MATCHDAY)

    if new_matchday != current_matchday.matchday:
        # update new matchday
        raw_match_data = get_all_info_for_matchday(new_matchday)
        new_matchday.save()
        update_matchday(raw_match_data, new_update_time, new_matchday)
        # TODO check for old match date update as well..
        # something might have happened during the match day swap
    else:  # handle same match day but newly updated
        if new_update_time > current_matchday.last_update:
            raw_match_data = get_all_info_for_matchday(new_matchday)
            update_matchday(raw_match_data, new_update_time, current_matchday)

    reload_cache()


def update_matchday(
    raw_match_data,
    new_update_time: datetime,
    current_matchday: MatchDayMetadata
):
    match_ids = (match['MatchID'] for match in raw_match_data)
    current_match_data = list(Match.objects
                              .filter(external_id__in=match_ids)
                              .select_related('team_1')
                              .select_related('team_2')
                              )

    team_mapping = external_teams_mapping(current_match_data)
    match_mapping = external_match_mapping(current_match_data)

    # Get all goals related to each match received over the network
    # and insert any missing ones in the database
    # TODO it's unlikely but some goals might have been deleted.
    # TODO Might want to add that
    for external_match_data in raw_match_data:
        exteral_match_id = external_match_data['MatchID']
        internal_match = match_mapping[exteral_match_id]
        internal_team_1 = team_mapping[external_match_data['Team1']['TeamId']]
        internal_team_2 = team_mapping[external_match_data['Team2']['TeamId']]
        current_goals_recorded_for_match = Goal.objects.filter(
            match_id=internal_match.id
        )
        current_goals_recorded_for_match = {
            g.external_id: g for g in current_goals_recorded_for_match}

        new_goals, score_team_1, score_team_2 = transform_goals(
            external_match_data['Goals'],
            internal_team_1.id,
            internal_team_2.id,
            internal_match.id
        )
        Goal.objects.bulk_create([
            goal
            for goal in new_goals
            if goal.external_id not in current_goals_recorded_for_match
        ])

        # If the match is finished we need to calculate the outcomes
        # and insert them into the db
        if external_match_data['MatchIsFinished'] \
                and not internal_match.finished:
            internal_match.finished = True
            internal_match.last_update_utc = western_europe_time_to_utc(
                external_match_data['LastUpdateDateTime'])
            internal_match.save()

            all_outcomes = get_outcomes(
                internal_match,
                internal_team_1,
                internal_team_2,
                score_team_1,
                score_team_2)
            Outcome.objects.bulk_create(all_outcomes)

            current_matchday.last_update = new_update_time
            current_matchday.save()


def poll_for_new_match_data():
    if not Task.objects.filter(verbose_name='poll_for_mach_data').exists():
        update_matches_if_necessary(
            repeat=Task.HOURLY,
            repeat_until=None,
            verbose_name='poll_for_mach_data'
        )
