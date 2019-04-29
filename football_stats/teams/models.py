from django.db import models


class Team(models.Model):
    external_id = models.IntegerField(unique=True)
    team_name = models.CharField(max_length=255)
    team_icon_url = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return str(self.team_name)
