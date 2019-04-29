from teams.providers.team_provider import pull_info_for_all_teams
from teams.services.network_data_team_parser import insert_into_database
from matches.services import network_data_match_parser
from matches.providers import match_provider
import time
import traceback
from matches.models import MatchDayMetadata

try:
    if len(MatchDayMetadata.objects.all()) == 0:
        teams = pull_info_for_all_teams(2018)
        teams_id_map = insert_into_database(teams)

        print('Sleeping for 5 seconds after the team request')
        time.sleep(5)

        matches = match_provider.pull_info_for_all_matches(2018)

        locations_id_map = network_data_match_parser.insert_locations_into_database(
            matches)
        matches_id_map = network_data_match_parser.insert_matches_into_database(
            matches, locations_id_map, teams_id_map)
        network_data_match_parser.insert_goals_into_database(
            matches, matches_id_map, teams_id_map)

        print('Sleeping for 5 seconds after the matches request')
        time.sleep(5)

        match_provider.pull_current_match_day_metadata().save()


except Exception as e:
    traceback.print_exc()
