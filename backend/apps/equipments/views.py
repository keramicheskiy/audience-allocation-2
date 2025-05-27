from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.auth.decorators import role_required
from apps.equipments.models import Equipment
from apps.equipments.serializers import EquipmentSerializer


# localhost:8080/equipments
@api_view(["GET"])
@role_required("teacher")
def get_equipments(request):
    serializer = EquipmentSerializer(Equipment.objects.all(), many=True)
    return Response({"equipments": serializer.data}, status=status.HTTP_200_OK)


# localhost:8080/equipments/new
# {"name": ""}
@api_view(["POST"])
@role_required("moderator")
def create_equipment(request):
    serializer = EquipmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/equipments/<equipment_id>
# {"name": ""}
@api_view(["GET", "PATCH", "DELETE"])
@role_required("moderator")
def manage_equipment(request, equipment_id):
    if request.method == "GET":
        return Response({"fields": EquipmentSerializer.fields})
    elif request.method == "PATCH":
        equipment = get_object_or_404(Equipment, pk=equipment_id)
        serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        equipment = get_object_or_404(Equipment, pk=equipment_id)
        equipment.delete()
        return Response(status=status.HTTP_200_OK)
