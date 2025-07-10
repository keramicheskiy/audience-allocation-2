from django.shortcuts import get_object_or_404
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication.serializers import CustomUserSerializer, RegistrationSerializer, LoginSerializer
from apps.authentication import utils, tasks
from apps.authentication.decorators import authenticated, role_required
from apps.authentication.models import CustomUser
from apps.authentication.services import verify_email, notify_moderators
from apps.role_approvance_requests.models import RoleForApproving


# localhost:8080/auth/register
# {"first_name": "", "patronymic": "", "last_name": "", "email": "", "password": "", "role": ""}
@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return Response({"fields": RegistrationSerializer.Meta.fields})

    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            token = Token.objects.create(user=user)
            verify_email(user)
            notify_moderators(user)

            return Response({
                'token': token.key, 'users': CustomUserSerializer(user).data}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/auth/login
# {"email": "", "password": ""}
@api_view(["GET", "POST"])
def login(request):
    if request.method == 'GET':
        return Response({"fields": LoginSerializer.Meta.fields})
    elif request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email и пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, email=email)
        if not user.check_password(password):
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': CustomUserSerializer(user).data})


# localhost:8080/auth/verify-token
@api_view(['GET'])
@authenticated()
def verify_token(request):
    user = utils.get_user_from_request(request)
    return Response({"user": CustomUserSerializer(user).data}, status=status.HTTP_200_OK)


# localhost:8080/auth/role/is-confirmed
@api_view(['GET'])
@role_required('teacher')
def is_role_confirmed(request):
    user = utils.get_user_from_request(request)
    if RoleForApproving.objects.find(user=user).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response({"role": str(user.role)}, status=status.HTTP_200_OK)
