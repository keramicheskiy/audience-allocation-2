from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('dashboard', views.dashboard),  # ТУТ ДОЛЖЕН БЫТЬ Список аудиторий, фильтр по времени, кнопка брони
    path('booking', views.booking),
    path('profile', views.profile),
    path('', views.home),
    path('', views.home),
    path('', views.home),
    path('', views.home),
]

