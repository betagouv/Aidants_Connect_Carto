from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from aidants_connect_carto_api.models import Place, Service
from aidants_connect_carto_api.serializers import PlaceSerializer, ServiceSerializer


@api_view(['GET'])
def place_list(request):
    """
    List all places
    """
    places = Place.objects.all()

    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def place_detail(request, pk):
    """
    Retrieve a place
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PlaceSerializer(place)
    return Response(serializer.data)
