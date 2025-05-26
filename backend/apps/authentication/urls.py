from django.urls import path

from apps.authentication import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('verify-token', views.verify_token),
    path('role/is-assigned', views.is_role_assigned),

]
