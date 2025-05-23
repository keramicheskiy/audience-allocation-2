from django.urls import path
import views

urlpatterns = [
    path("requests", views.role_approving_requests),
    path("requests/<request_id>", views.role_approvance),
    path("users", views.get_all_users),
    path("users/<user_id>/set_role", views.change_role),
    path("users/<user_id>", views.manage_user),
]
