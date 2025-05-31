from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('main', views.main),
    path('help', views.rest),
    path('rest', views.rest),
    path('profile', views.profile),
    path('profile/lectures', views.my_lectures),
    path('lectures', views.all_lectures),
    path('available-auditoriums', views.available_auditoriums),
    path('auditoriums', views.all_auditoriums),
    path('equipments', views.equipments),
    path('users', views.get_users),
    path('users/<user_id>', views.get_user),
    path('requests', views.role_approvance_requests),
]