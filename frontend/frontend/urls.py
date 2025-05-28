from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("apps.home.urls")),
    path('auth/', include('apps.authentication.urls')),
    path('profile', include('apps.users.urls')),
]
