from django.shortcuts import render

# Create your views here.


def home(request):

    # TODO ДОБРО ПОЖАЛОВАТЬ ТАМ ХЗ ВоЙТИ ЗАРЕГАТЬСЯ, ЛОГОТИП НАЗВАНИЕ, КРАТКОЕ ОПИСАНИЕ
    return render(request, "home/home.html")
