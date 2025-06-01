from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from frontend import settings

urlpatterns = [
    path('', include("apps.home.urls")),
    path('auth/', include('apps.authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


