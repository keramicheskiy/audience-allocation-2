from django.http import HttpResponse
from django.shortcuts import render
import requests
from frontend.settings import BACKEND_URL
from .decorators import authenticated


def register(request):
    return render(request, "authentication/register.html")


def login(request):
    return render(request, "authentication/login.html")


@authenticated()
def verify_token(request):
    cookies = {'Token': request.COOKIES.get('Token')}
    response = requests.get(BACKEND_URL + '/auth/verify-token', cookies=cookies)

    if response.status_code == 200:
        return HttpResponse(f"Passed for {request.COOKIES.get('Token')} ({response.json()})")
    return HttpResponse(f"Token cannot not be verified! ({request.COOKIES.get('Token')}")
