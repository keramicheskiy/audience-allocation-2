from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("apps.home.urls")),
    path('teachers', include('apps.teachers.urls')),
    path('auth', include('apps.authentication.urls')),
    path('profile', include('apps.user.urls')),
]
