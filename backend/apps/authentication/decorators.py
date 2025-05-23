from celery.bin.control import status
from django.http import HttpResponseForbidden
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from backend.settings import permitted_roles


def authenticated(func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('token')
        if not token or not Token.objects.filter(token=token).exists():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        func(request, *args, **kwargs)

    return wrapper


def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            token = request.COOKIES.get('token')
            if token and Token.objects.filter(token=token).exists():
                user = Token.objects.get(token=token).user
                if user.role in permitted_roles(role):
                    return view_func(request, *args, **kwargs)
                return HttpResponseForbidden("Ваша роль не подходит для данного действия или еще не была подтверждена.")
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return _wrapped_view

    return decorator
