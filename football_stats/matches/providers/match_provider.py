import requests
from matches.providers.matches_cache import matches
from typing import List, Any, Dict


def pull_info_for_all_matches(year: int) -> List[Dict[Any, Any]]:
    # url = 'https://www.openligadb.de/api/getmatchdata/bl1/{}'.format(year)
    # headers = {'Content-Type': 'application/json'}
    # response = requests.get(url, headers=headers)

    # return response.json()
    return matches


def pull_matchday_metadata():
    url = 'https://www.openligadb.de/api/getcurrentgroup/bl1'
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()


def pull_current_matchday_last_change(year: int, matchday: int):
    url = "https://www.openligadb.de/api/getlastchangedate/bl1/{}/{}".format(
        year, matchday
    )
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.text
