from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('teams.urls')),
    path('season/', include('matches.urls'))
]
