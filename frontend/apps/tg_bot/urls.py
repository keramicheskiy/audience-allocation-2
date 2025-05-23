from django.urls import path

import views

urlpatterns = [
    path("", views.info),
    path("info", views.info),
]
