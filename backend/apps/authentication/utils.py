from rest_framework.authtoken.models import Token


def get_user_from_request(request):
    return Token.objects.get(key=request.COOKIES.get('Token')).user
