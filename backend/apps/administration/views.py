from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.administration.models import RoleForApproving
from apps.administration.serializers import RoleForApprovingSerializer
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.authentication.serializers import CustomUserSerializer


# localhost:8080/administration/requests
@api_view(['GET'])
@role_required("admin")
def role_approving_requests(request):
    approving_requests = RoleForApproving.objects.all()
    return Response({'requests': RoleForApprovingSerializer(approving_requests, many=True).data})


# localhost:8080/administration/requests/<request_id>
# {}
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


# localhost:8080/administration/users
@api_view(['GET'])
@role_required("admin")
def get_all_users(request):
    users = CustomUser.objects.all()
    return Response({"users": CustomUserSerializer(users, many=True).data})


# localhost:8080/administration/users/<user_id>/role/approve
# {"role": ""}
@api_view(['PATCH'])
@role_required("admin")
def change_role(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    role = request.data.get('role')
    if not role:
        return Response({"detail": "Роль не указана."}, status=status.HTTP_400_BAD_REQUEST)
    new_role = user.assign_role(role)
    return Response({"role": new_role}, status=status.HTTP_200_OK)


# localhost:8080/administration/users/{user_id}
@api_view(["DELETE"])
@role_required("admin")
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
