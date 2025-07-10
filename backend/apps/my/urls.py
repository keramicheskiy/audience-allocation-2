from django.urls import path
from . import views

urlpatterns = [
    path('lectures', views.get_own_lectures),
    path('lectures/upcoming', views.get_my_upcoming_lectures),
    path('profile', views.get_profile),
]
