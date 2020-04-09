import requests as python_request

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from aidants_connect_carto_api.models import Place
from aidants_connect_carto_api.serializers import PlaceSerializer


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "places": reverse("place-list", request=request),
            # 'services': reverse('service-list', request=request, format=format)
        }
    )


class PlaceList(APIView):
    """
    List all places, or create a new place.
    """

    def get(self, request, format=None):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlaceSerializer)
    def post(self, request, format=None):
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
        place = get_object_or_404(Place, pk=pk)
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlaceSerializer)
    def put(self, request, pk, format=None):
        place = get_object_or_404(Place, pk=pk)
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        place = get_object_or_404(Place, pk=pk)
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


q_param = openapi.Parameter(
    "q", openapi.IN_QUERY, description="search query", type=openapi.TYPE_STRING
)


@swagger_auto_schema(method="get", manual_parameters=[q_param])
@api_view(["GET"])
def address_search(request):
    """
    https://adresse.data.gouv.fr/
    """
    results = python_request.get(
        f"{settings.BAN_ADDRESS_SEARCH_API}?q={request.GET.get('q')}"
    )
    return Response(results.json())
