from django.contrib import admin
from django.urls import path, include
# from .background_tasks import poll_for_mach_data
from teams.services.team_service import reload_cache

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('teams.urls')),
    path('season/', include('matches.urls'))
]

# reload_cache()
# poll_for_mach_data()
