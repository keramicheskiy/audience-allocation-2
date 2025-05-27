from django.urls import path

import views

urlpatterns = [
    path('users', views.get_users),
    path('users/<user_id>', views.get_user),
    path('users/<user_id>/delete', views.delete_user),
    path("users/<user_id>/lectures", views.lectures_from_teacher),
    path("users/<user_id>/auditoriums/<auditorium_id>", views.manage_allowed_auditorium),
    path("users/<user_id>/auditoriums", views.reset_allowed_auditoriums),
    path("users/<user_id>/limit/hours", views.limit_amount_of_hours),
    path("users/<user_id>/limit/auditoriums", views.limit_amount_of_auditoriums),
    path("users/<user_id>/role", views.change_role),
]
