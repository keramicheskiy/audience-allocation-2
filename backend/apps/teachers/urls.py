from django.urls import path

from apps.teachers import views

urlpatterns = [
    path('book/{auditorium_id}', views.book_auditorium, name='index'),
]
