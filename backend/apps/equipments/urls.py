from django.urls import path

import views

urlpatterns = [
    path('equipments', views.get_equipments),
    path("equipments/new", views.create_equipment),
    path("equipments/<equipment_id>", views.manage_equipment),
]
