from django.shortcuts import render
from django.http import HttpRequest
from teams.services.team_service import (
    get_leaderboard, get_teams_by_name_similarity, get_team)
from typing import List
from teams.services.domain import TeamRepresentation

# Create your views here.


def index(request: HttpRequest):
    teams = get_leaderboard()
    return render(request, 'index.html', {'teams': teams})


def team_search(request: HttpRequest):
    team_query = request.GET.get('team')
    teams: List[TeamRepresentation] = []
    if team_query is not None:
        teams = get_teams_by_name_similarity(team_query)
    return render(request, 'teams/search.html', {'teams': teams})


def team(request: HttpRequest, team_id: int):
    team = get_team(team_id)
    return render(request, 'teams/team.html', {'team': team})
