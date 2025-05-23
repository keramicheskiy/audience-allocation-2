from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('administration/', include("apps.administration.urls")),
    path('teachers/', include('apps.teachers.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('moderation/', include('apps.moderation.urls')),
]

