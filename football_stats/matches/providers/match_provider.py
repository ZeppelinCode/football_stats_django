import requests
from matches.providers.matches_cache import matches
from matches.models import MatchDayMetadata
from typing import List, Any, Dict
from util.util import western_europe_time_to_utc


def pull_info_for_all_matches(year: int) -> List[Dict[Any, Any]]:
    # url = 'https://www.openligadb.de/api/getmatchdata/bl1/{}'.format(year)
    # headers = {'Content-Type': 'application/json'}
    # response = requests.get(url, headers=headers)

    # return response.json()
    return matches


def pull_current_matchday():
    url = 'https://www.openligadb.de/api/getcurrentgroup/bl1'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()


def get_all_info_for_matchday(matchday: int, year: int = 2018):
    url = 'https://www.openligadb.de/api/getmatchdata/bl1/{}/{}'.format(
        year, matchday)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()


def pull_current_matchday_last_change(year: int, matchday: int):
    url = "https://www.openligadb.de/api/getlastchangedate/bl1/{}/{}".format(
        year, matchday
    )
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()


def pull_current_match_day_metadata() -> MatchDayMetadata:
    match_day_metadata = pull_current_matchday()
    last_update_for_matchday = pull_current_matchday_last_change(
        2018,
        match_day_metadata['GroupOrderID']
    )
    return MatchDayMetadata(
        matchday=match_day_metadata['GroupOrderID'],
        last_update=western_europe_time_to_utc(last_update_for_matchday)
    )
