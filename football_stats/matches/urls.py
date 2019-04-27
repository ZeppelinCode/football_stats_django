from matches import views
from django.urls import path

urlpatterns = [
    path('matches', views.get_all_season_matches, name='season'),
    path('upcomming-matches', views.get_upcomming_matches,
         name='upcomming_matches'),
]
