from django.urls import path
from . import views

urlpatterns = [
    path("", views.role_approving_requests),
    path("<request_id>", views.role_approvance),
]
