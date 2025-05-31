from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication import tasks
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.authentication.serializers import CustomUserSerializer
from apps.role_approvance_requests.models import RoleForApproving
from apps.role_approvance_requests.serializers import RoleForApprovingSerializer


# localhost:8080/requests
@api_view(['GET'])
@role_required("admin")
def role_approving_requests(request):
    approving_requests = RoleForApproving.objects.all()
    return Response({'requests': RoleForApprovingSerializer(approving_requests, many=True).data})


# localhost:8080/requests/<request_id>
# {}
@api_view(['PATCH', 'DELETE'])
@role_required("admin")
def role_approvance(request, request_id):
    request_for_approvance = get_object_or_404(RoleForApproving, pk=request_id)
    user = request_for_approvance.user
    if request.method == 'PATCH':
        user.assign_role(request_for_approvance.wannabe_role)
        user.save()
        if user.tg_id:
            tasks.send_telegram_message.delay("Ваша новая роль была подтверждена", user.tg_id)
        request_for_approvance.delete()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if user.tg_id:
            tasks.send_telegram_message.delay("Администратор отклонил выбранную вами роль", user.tg_id)
        request_for_approvance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
