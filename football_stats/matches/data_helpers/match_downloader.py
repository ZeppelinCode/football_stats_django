import requests
from typing import List, Dict, Any, Generator, Tuple
from matches.data_helpers.matches_cache import matches
from matches.models import Match, Location
from itertools import groupby


def pull_info_for_all_matches(year: int) -> List[Dict[Any, Any]]:
    # url = 'https://www.openligadb.de/api/getmatchdata/bl1/{}'.format(year)
    # headers = {'Content-Type': 'application/json'}
    # response = requests.get(url, headers=headers)

    # return response.json()
    return matches


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
        raw_location_to_model_location=Dict[int, Location]) -> Match:

    match_location = None
    if raw_match['Location']:
        external_location_id = raw_match['Location']['LocationID']
        match_location = raw_location_to_model_location[external_location_id]

    # TODO handle time formats, last_update is not utc..
    return Match(
        external_id=raw_match['MatchID'],
        match_time_utc=raw_match['MatchDateTimeUTC'],
        location=match_location,
        viewers=raw_match['NumberOfViewers'],
        last_update=raw_match['LastUpdateDateTime'],
        finished=raw_match['MatchIsFinished'])


def insert_matches_into_database(
        raw_matches: List[Dict[Any, Any]],
        raw_location_to_model_location=Dict[int, Location]) -> Match:

    matches = (raw_match_to_match_model(
        raw_match, raw_location_to_model_location)
        for raw_match in raw_matches)
    Match.objects.bulk_create(matches)
