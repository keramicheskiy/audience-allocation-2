from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_auditoriums),  # ?date=2025-12-31&start=10:45&end=12:15
    path("new", views.create_auditorium),
    path('<auditorium_id>', views.get_auditorium),
    path("<auditorium_id>/update", views.update_auditorium),
    path("<auditorium_id>/delete", views.delete_auditorium),
    path('<auditorium_id>/book', views.book_auditorium),
]
