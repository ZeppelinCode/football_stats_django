from django.shortcuts import render
from django.http import HttpRequest
from logic.services.leaderboard_service import get_leaderboard


def index(request: HttpRequest):
    leaderboard = get_leaderboard()
    return render(request, 'index.html', {'leaderboard': leaderboard})
