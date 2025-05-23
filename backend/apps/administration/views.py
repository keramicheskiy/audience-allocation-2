from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.administration.models import RoleForApproving
from apps.administration.serializers import RoleForApprovingSerializer
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.authentication.serializers import CustomUserSerializer


@api_view(['GET'])
@role_required("admin")
def role_approving_requests(request):
    approving_requests = RoleForApproving.objects.all()
    return Response({'requests': RoleForApprovingSerializer(approving_requests, many=True).data})


@api_view(['PATCH', 'DELETE'])
@role_required("admin")
def role_approvance(request, request_id):
    request_for_approvance = get_object_or_404(RoleForApproving, pk=request_id)
    if request.method == 'PATCH':
        user = request_for_approvance.user
        user.assign_role(request_for_approvance.wannabe_role)
        user.save()
        request_for_approvance.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        request_for_approvance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@role_required("admin")
def get_all_users(request):
    users = CustomUser.objects.all()
    return Response({"users": CustomUserSerializer(users, many=True).data})


@api_view(['PATCH'])
@role_required("admin")
def change_role(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    role = request.data.get('role')
    if not role:
        return Response({"detail": "Роль не указана."}, status=status.HTTP_400_BAD_REQUEST)
    new_role = user.assign_role(role)
    return Response({"role": new_role}, status=status.HTTP_200_OK)


@api_view(["GET", "DELETE"])
@role_required("admin")
def manage_user(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(CustomUser, pk=user_id)
        return Response({"user": CustomUserSerializer(user).data}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
