from django.urls import path

import views

urlpatterns = [
    path("lectures", views.get_lectures),
]
