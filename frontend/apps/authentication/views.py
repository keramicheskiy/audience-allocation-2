from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import forms
import requests
from frontend.settings import BACKEND_URL
from .decorators import authenticated


def register(request):
    if request.method == 'GET':
        return render(request, "authentication/registration.html",
                      context={"form": forms.RegistrationForm})
    elif request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            result = requests.post(url=BACKEND_URL + "/authentication/register", json=form.cleaned_data)
            if result.status_code == 201:
                token = result.json()['token']
                redirection = redirect(to="/profile")
                redirection.set_cookie(
                    "Token",
                    token.key,
                    max_age=60 * 60 * 24 * 30,
                    httponly=True,
                    samesite="Lax",
                )
                return redirection
            return HttpResponse(f"{result.status_code}, {result.text}")
        return HttpResponse(form.errors, status=400)


def login(request):
    if request.method == 'GET':
        return render(request, "authentication/login.html",
                      context={"form": forms.LoginForm})
    elif request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            result = requests.post(url=BACKEND_URL + "/authentication/login", json=form.cleaned_data)
            if result.status_code == 200:
                token = result.json()['token']
                redirection = redirect(to="/profile")
                redirection.set_cookie(
                    "Token",
                    token.key,
                    max_age=60 * 60 * 24 * 30,
                    httponly=True,
                    samesite="Lax",
                )
                return redirection
            return HttpResponse(f"{result.status_code}, {result.text}")
        return HttpResponse(form.errors, status=400)


@authenticated()
def verify_token(request):
    cookies = {'Token': request.COOKIES.get('Token')}
    response = requests.get(BACKEND_URL + '/authentication/verify-token', cookies=cookies)

    if response.status_code == 200:
        return HttpResponse(f"Passed for {request.COOKIES.get('Token')}")
    return HttpResponse(f"Token cannot not be verified!")
