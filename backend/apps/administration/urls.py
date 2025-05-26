from django.urls import path
from . import views

urlpatterns = [
    path("requests", views.role_approving_requests),
    path("requests/<request_id>", views.role_approvance),
    path("users", views.get_all_users),
    path("users/<user_id>/role/approve", views.change_role),
    path("users/<user_id>", views.delete_user),
]
