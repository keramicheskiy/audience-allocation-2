from django.urls import path

from apps.auth import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('verify-token', views.verify_token),
    path('role/is-confirmed', views.is_role_confirmed),
]
