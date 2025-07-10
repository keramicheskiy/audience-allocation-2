from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('main', views.main),
    path('profile', views.profile),
    path('profile/lectures', views.my_lectures),
    path('lectures', views.all_lectures),
    path('booking', views.available_auditoriums),
    path('auditoriums', views.all_auditoriums),
    path('equipments', views.equipments),
    path('buildings', views.buildings),
    path('users', views.get_users),
    path('users/<user_id>', views.get_user),
    path('roles/requests', views.role_approvance_requests),
    path('booking/requests', views.booking_requests),

]
