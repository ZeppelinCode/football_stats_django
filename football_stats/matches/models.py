from django.db import models
from django.utils import timezone
from teams.models import Team


class Location(models.Model):
    external_id = models.IntegerField(unique=True)
    city = models.CharField(max_length=255, null=True)
    stadium = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{}:{}".format(str(self.city), str(self.stadium))


class Match(models.Model):
    external_id = models.IntegerField(unique=True)
    match_time_utc = models.DateTimeField(null=True)
    league_name = models.CharField(max_length=255, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=True)
    viewers = models.IntegerField(null=True)
    last_update = models.DateTimeField(null=True)
    finished = models.BooleanField(default=False)
    team_1 = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name='fk_team_1')
    team_2 = models.ForeignKey(
        Team, on_delete=models.PROTECT, related_name='fk_team_2')

    class Meta:
        indexes = [
            models.Index(fields=['team_1']),
            models.Index(fields=['team_2']),
        ]

    def __str__(self) -> str:
        return str(self.team_name)


class Goal(models.Model):
    external_id = models.IntegerField(unique=True)
    goal_getter_name = models.CharField(max_length=255)
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    match_minute = models.IntegerField(null=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return "{}:{}'{}".format(
            self.match_id,
            str(self.goal_getter_name),
            self.match_minute)
