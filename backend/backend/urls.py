from django.contrib import admin
from django.urls import path, include

from backend import views

urlpatterns = [
    path('auditoriums/', include("apps.auditoriums.urls")),
    path('auth/', include('apps.authentication.urls')),
    path('equipments/', include('apps.equipments.urls')),
    path('lectures/', include('apps.lectures.urls')),
    path('my/', include('apps.my.urls')),
    path('requests/', include('apps.role_approvance_requests.urls')),
    path('users/', include('apps.users.urls')),
    path('health', views.health),
]

