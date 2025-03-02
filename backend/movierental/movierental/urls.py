from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),
    path('rentals/', include('rentals.urls')),
]
