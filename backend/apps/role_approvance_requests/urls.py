from django.urls import path
from . import views

urlpatterns = [
    path("requests", views.role_approving_requests),
    path("requests/<request_id>", views.role_approvance),
]
