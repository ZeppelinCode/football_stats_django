from django.apps import AppConfig


class TeamsConfig(AppConfig):
    name = 'teams'

    # warm up the cache on startup
    def ready(self):
        from teams.services.team_service import reaload_cache
        reaload_cache()
