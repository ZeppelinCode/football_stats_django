from matches import views
from django.urls import path

urlpatterns = [
    path('', views.get_all_season_matches, name='season'),
]
