from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_lectures),
    path("upcoming", views.get_all_upcoming_lectures),
    path("<lecture_id>", views.delete_lecture),
]
