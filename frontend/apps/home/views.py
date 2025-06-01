import requests
from django.shortcuts import render, redirect

from apps.authentication import utils
from apps.authentication.decorators import authenticated, role_required
from frontend.settings import BACKEND_URL


def home(request):
    return render(request, "home/home.html")



@authenticated()
def main(request):
    response = requests.get(url=BACKEND_URL + "/my/profile", cookies=request.COOKIES)
    context = {"user": response.json()}
    return render(request, "base.html", context=context)


@role_required("moderator")
def all_lectures(request):
    return render(request, "home/all_lectures.html")


@authenticated()
def my_lectures(request):
    return render(request, "home/my_lectures.html")


@authenticated()
def available_auditoriums(request):
    return render(request, "home/booking.html")


@role_required("moderator")
def all_auditoriums(request):
    return render(request, "home/all_auditoriums.html")


@role_required("moderator")
def equipments(request):
    return render(request, "home/equipments.html")


@role_required("moderator")
def get_users(request):
    return render(request, "home/users.html")


@authenticated()
def role_approvance_requests(request):
    return render(request, "home/requests.html")


@authenticated()
def get_user(request, user_id):
    return render(request, "home/profile.html", context={"user_id": user_id})


@authenticated()
def profile(request):
    response = requests.get(url=BACKEND_URL + "/my/profile", cookies=request.COOKIES)
    user = response.json()["user"]
    return redirect(f"/users/{user['id']}")
