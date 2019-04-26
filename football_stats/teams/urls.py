from teams import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='leaderboard'),
    path('team/search', views.team_search, name='team_search'),
    path('team/<int:team_id>', views.team, name='team'),
]
