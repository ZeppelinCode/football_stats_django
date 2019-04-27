from teams.data_helpers import team_downloader
from matches.data_helpers import match_downloader
from matches.providers import match_provider
import traceback

try:
    teams = team_downloader.pull_info_for_all_teams(2018)
    teams_id_map = team_downloader.insert_into_database(teams)

    matches = match_provider.pull_info_for_all_matches(2018)

    locations_id_map = match_downloader.insert_locations_into_database(matches)
    matches_id_map = match_downloader.insert_matches_into_database(
        matches, locations_id_map, teams_id_map)
    match_downloader.insert_goals_into_database(
        matches, matches_id_map, teams_id_map)

    match_day_metadata = match_provider.pull_matchday_metadata()
    last_update_for_matchday = match_provider\
        .pull_current_matchday_last_change(
            2018,
            match_day_metadata['GroupOrderID']
        )
    match_downloader.insert_matchday_info(
        match_day_metadata, last_update_for_matchday)


except Exception as e:
    traceback.print_exc()
