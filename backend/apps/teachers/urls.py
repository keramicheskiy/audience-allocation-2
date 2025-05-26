from django.urls import path

from apps.teachers import views

urlpatterns = [
    path('equipments', views.get_equipments),
    path('my/lectures', views.get_own_lectures),
    path('my/lectures/upcoming', views.get_upcoming_lectures),
    path('auditoriums', views.get_free_auditoriums),
    path('auditoriums/<auditorium_id>/book', views.book_auditorium),
    path('auditoriums/<auditorium_id>', views.get_auditorium),
    path('users/{user_id}', views.get_user),
]
