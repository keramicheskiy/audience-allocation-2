from django.urls import path
from . import views

urlpatterns = [
    path("new", views.create_auditorium),
    path("", views.get_auditoriums),
    path('<auditorium_id>', views.get_auditorium),
    path("<auditorium_id>/update", views.update_auditorium),
    path("<auditorium_id>/delete", views.delete_auditorium),
]
