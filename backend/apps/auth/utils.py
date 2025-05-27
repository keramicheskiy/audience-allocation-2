from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


def get_user_from_request(request):
    return Token.objects.get(key=request.COOKIES.get('Token')).user
