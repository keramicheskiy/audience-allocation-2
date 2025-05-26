from django.urls import path

from apps.moderation import views

urlpatterns = [
    # Lectures
    path("lectures", views.get_lectures),

    # Auditoriums
    path("auditoriums/new", views.create_auditorium),
    path("auditoriums/<auditorium_id>", views.manage_auditorium),

    # Equipment
    path("equipments/new", views.create_equipment),
    path("equipments/<equipment_id>", views.manage_equipment),

    # Users
    path("users/<user_id>/lectures", views.lectures_from_teacher),
    path("users/<user_id>/auditoriums", views.manage_allowed_auditoriums),
    path("users/<user_id>/auditoriums/<auditorium_id>", views.delete_allowed_auditorium),
    path("users/<user_id>/hours/limit", views.limit_amount_of_hours),
    path("users/<user_id>/auditoriums/limit", views.limit_amount_of_auditoriums),

]
