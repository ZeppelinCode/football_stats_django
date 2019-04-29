from django.contrib import admin
from matches.models import Match, Outcome, Goal, Location, MatchDayMetadata

admin.site.register(Match)
admin.site.register(Outcome)
admin.site.register(Goal)
admin.site.register(Location)
admin.site.register(MatchDayMetadata)
