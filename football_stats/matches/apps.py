from django.apps import AppConfig


class MatchesConfig(AppConfig):
    name = 'matches'

    def ready(self):
        # This will fail before the db is created
        try:
            import matches.services.background_match_service as bms
            bms.poll_for_new_match_data()
        except Exception as e:
            print(e)
