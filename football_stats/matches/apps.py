from django.apps import AppConfig


class MatchesConfig(AppConfig):
    name = 'matches'

    def ready(self):
        # This will fail before the db is created
        try:
            from matches.services.background_match_service import (
                poll_for_match_data)
            poll_for_match_data()
        except:
            pass
