from django.core.cache import cache
from teams.services.team_service import get_cached_value, reaload_cache
from background_task import background


@background
def update_matches_if_necessary(match_day_metadata):
    pass
    # current_matchday = get_cached_value('current_matchday')
    # if match_day_metadata.matchday != current_matchday.matchday:
    #     # update old match day, and set update time to now
    #     update_match(current_matchday)
    #     #  update new matchday
    #     update_match(match_day_metadata.matchday)

    # else:
    #     if match_day_metadata.last_update > current_matchday.last_update:
    #         update_match(current_matchday)

    # insert_new_matchday(match_day_metadata)
    # reaload_cache()
