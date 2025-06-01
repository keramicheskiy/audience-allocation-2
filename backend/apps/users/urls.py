from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_users),
    path('<user_id>', views.manage_user),
    path('<user_id>/delete', views.delete_user),
    path("<user_id>/lectures", views.lectures_from_teacher),
    path("<user_id>/lectures/<lecture_id>", views.delete_lecture),
    path("<user_id>/auditoriums", views.get_allowed_auditoriums),
    path("<user_id>/auditoriums/reset", views.reset_allowed_auditoriums),
    path("<user_id>/limit/hours", views.limit_amount_of_hours),
    path("<user_id>/limit/auditoriums", views.limit_amount_of_auditoriums),
    path("<user_id>/role", views.change_role),
    path("<user_id>/wannabe ", views.get_wannabe),
]
