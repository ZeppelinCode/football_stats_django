from teams.data_helpers import team_downloader
from matches.services import network_data_match_parser
from matches.providers import match_provider
import traceback

try:
    teams = team_downloader.pull_info_for_all_teams(2018)
    teams_id_map = team_downloader.insert_into_database(teams)

    matches = match_provider.pull_info_for_all_matches(2018)

    locations_id_map = network_data_match_parser.insert_locations_into_database(
        matches)
    matches_id_map = network_data_match_parser.insert_matches_into_database(
        matches, locations_id_map, teams_id_map)
    network_data_match_parser.insert_goals_into_database(
        matches, matches_id_map, teams_id_map)

    match_provider.pull_current_match_day_metadata().save()


except Exception as e:
    traceback.print_exc()
