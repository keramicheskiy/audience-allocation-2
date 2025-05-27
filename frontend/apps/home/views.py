from django.shortcuts import render

from apps.auth.decorators import authenticated


# Create your views here.

def home(request):
    # TODO ДОБРО ПОЖАЛОВАТЬ ТАМ ХЗ ВоЙТИ ЗАРЕГАТЬСЯ, ЛОГОТИП НАЗВАНИЕ, КРАТКОЕ ОПИСАНИЕ
    return render(request, "home/home.html")


@authenticated
def main(request):

    return render(request, "base.html")
