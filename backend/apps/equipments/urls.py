from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_equipments),
    path("new", views.create_equipment),
    path("<equipment_id>", views.manage_equipment),
]
