from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication.decorators import role_required
from .models import Building
from .serializers import BuildingSerializer


# localhost:8080/buildings
@api_view(["GET"])
@role_required("teacher")
def get_buildings(request):
    serializer = BuildingSerializer(Building.objects.all(), many=True)
    return Response({"buildings": serializer.data}, status=status.HTTP_200_OK)


# localhost:8080/buildings/new
# {"name": ""}
@api_view(["POST"])
@role_required("moderator")
def create_building(request):
    serializer = BuildingSerializer(data=request.data)
    if serializer.is_valid():
        if Building.objects.filter(name=serializer.validated_data["name"]).exists():
            return Response({"message": "Название не уникально"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/buildings/<building_id>
# {"name": ""}
@api_view(["GET", "PATCH", "DELETE"])
@role_required("moderator")
def manage_building(request, building_id):
    if request.method == "GET":
        building = get_object_or_404(Building, pk=building_id)
        return Response(BuildingSerializer(building).data)
    elif request.method == "PATCH":
        building = get_object_or_404(Building, pk=building_id)
        serializer = BuildingSerializer(building, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        building = get_object_or_404(Building, pk=building_id)
        building.delete()
        return Response(status=status.HTTP_200_OK)
