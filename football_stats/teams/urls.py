from teams import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='teams'),
    path('team/<int:id>', views.team, name='team'),
]
