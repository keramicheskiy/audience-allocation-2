from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_buildings),
    path("new", views.create_building),
    path("<building_id>", views.manage_building),
]
