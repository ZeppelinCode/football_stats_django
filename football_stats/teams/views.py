from django.shortcuts import render
from teams.models import Team
from matches.models import Outcome
from django.db.models import Count


# Create your views here.


def index(request):
    leaderboard = calculate_leaderboard()
    return render(request, 'index.html', {'leaderboard': leaderboard})


def team():
    pass


def calculate_leaderboard():
    outcomes = Outcome.objects.values(
        'team__team_name',
        'outcome_type'
    ).annotate(outcome_type_count=Count('outcome_type'))

    team_performances = {}
    for outcome in outcomes:
        team_name = outcome['team__team_name']
        team_performance = team_performances.get(
            team_name, {'team_name': team_name})
        team_performance[outcome['outcome_type']
                         ] = outcome['outcome_type_count']
        team_performances[team_name] = team_performance

    calculate_and_add_points(team_performances)

    return sorted(team_performances.values(), key=lambda tp: tp['points'], reverse=True)


def calculate_and_add_points(team_performances):
    for team_name, team_performance in team_performances.items():
        points = team_performance['win'] * 3 + team_performance['draw']
        team_performance['points'] = points
