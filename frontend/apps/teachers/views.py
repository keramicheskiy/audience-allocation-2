import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

from frontend.settings import BACKEND_URL
from ..authentication.decorators import role_required
from ..teachers.decorators import logged_in


# Create your views here.
# @logged_in

@role_required("teacher")
def dashboard(request):
    response = requests.get(url=BACKEND_URL + "/teachers/")

    # TODO СПИСОК АУДИТОРИЙ КОТОРЫЕ ПРЕПОД МОЖЕТ ЗАНЯТЬ
    return render(request, "teachers/dashboard.html")


@role_required("teacher")
def booking(request):
    # TODO САМО БРОНИРОВАНИЕ АУДИТОРИИ В УЖЕ ВЫБРАННОМ КАБИНЕТЕ ЕЩЕ НУЖНО ВЫВОДИТЬ СПИСОК УЖЕ ЗАБРОНИРОВАННЫХ
    # TODO АДУИТОРИЙ, ЗАНЯТИЯ В КОТОРЫХ ЕЩЕ НЕ ЗАКОНЧАЛИСЬ
    return render(request, "teachers/booking.html")


@role_required("teacher")
def profile(request):
    return redirect("/profile")


