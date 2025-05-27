from django.urls import path
import views

urlpatterns = [
    path('my/lectures', views.get_own_lectures),
    path('my/lectures/upcoming', views.get_upcoming_lectures),
]
