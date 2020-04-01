from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from aidants_connect_carto_api.models import Place, Service
from aidants_connect_carto_api.serializers import PlaceSerializer, ServiceSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'places': reverse('place-list', request=request),
        # 'services': reverse('service-list', request=request, format=format)
    })


class PlaceList(APIView):
    """
    List all places, or create a new place.
    """
    def get(self, request, format=None):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceDetail(APIView):
    """
    Retrieve, update or delete a place instance.
    """
    def get(self, request, pk, format=None):
        place = self.get_object_or_404(pk)
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        place = self.get_object_or_404(pk)
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        place = self.get_object_or_404(pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
