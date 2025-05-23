from django.urls import path

from apps.moderation import views

urlpatterns = [
    # Lectures
    path("lectures", views.get_lectures),

    # Auditoriums
    path("auditoriums/create", views.create_auditorium),
    path("auditoriums/<int:pk>/update", views.update_auditorium),
    path("auditoriums/<int:pk>/delete", views.delete_auditorium),

    # Equipment
    path("equipments/create", views.create_equipment),
    path("equipments/<int:pk>/update", views.update_equipment),
    path("equipments/<int:pk>/delete", views.delete_equipment),

]
