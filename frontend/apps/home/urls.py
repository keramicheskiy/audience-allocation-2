from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('main', views.main),
    path('help', views.rest),
    path('rest', views.rest),
]