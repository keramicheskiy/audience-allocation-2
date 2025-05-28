import requests
from django.http import HttpResponse
from django.shortcuts import render

from apps.authentication.decorators import authenticated, role_required
from frontend.settings import BACKEND_URL


# Create your views here.

def home(request):
    # TODO ДОБРО ПОЖАЛОВАТЬ ТАМ ХЗ ВоЙТИ ЗАРЕГАТЬСЯ, ЛОГОТИП НАЗВАНИЕ, КРАТКОЕ ОПИСАНИЕ
    return render(request, "home/home.html")


@authenticated()
def main(request):
    response = requests.get(url=BACKEND_URL + "/my/profile", cookies=request.COOKIES)
    context = {"user": response.json()}
    return render(request, "main.html", context=context)


def rest(request):
    return render(request, "home/rest.html")
