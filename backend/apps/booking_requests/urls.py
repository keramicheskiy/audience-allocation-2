from django.urls import path
from . import views


urlpatterns = [
    path("requests", views.get_booking_requests),
    path("requests/add", views.add_booking_request),
    path("requests/<request_id>", views.manage_booking_request),
]