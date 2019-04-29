from django.apps import AppConfig


class TeamsConfig(AppConfig):
    name = 'teams'

    def ready(self):
        # This will fail if the db does not exist (makemigrations)
        try:
            from teams.services.team_service import reload_cache
            reload_cache()
        except Exception as e:
            print(e)
