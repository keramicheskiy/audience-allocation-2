from django.urls import path

from . import views


urlpatterns = [
    path('', views.profile),
    path('booked', views.booked),
    path('', views.profile),
    path('', views.profile),
    path('', views.profile),
]