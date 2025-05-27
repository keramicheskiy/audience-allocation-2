from django.urls import path

import views

urlpatterns = [
    path('auditoriums', views.get_free_auditoriums),  # ?date=2025-12-31&start=10:45&end=12:15
    path('auditoriums/<auditorium_id>', views.get_auditorium),
    path("auditoriums/new", views.create_auditorium),
    path("auditoriums/<auditorium_id>/update", views.update_auditorium),
    path("auditoriums/<auditorium_id>/delete", views.delete_auditorium),
    path('auditoriums/<auditorium_id>/book', views.book_auditorium),
]
