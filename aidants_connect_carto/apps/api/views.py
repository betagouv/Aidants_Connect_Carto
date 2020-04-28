from django.shortcuts import get_object_or_404

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from aidants_connect_carto.apps.api.serializers import (
    DataSourceSerializer,
    PlaceSerializer,
    ServiceSerializer,
)
from aidants_connect_carto.apps.core.models import DataSource, Place  # Service
from aidants_connect_carto.apps.core.utilities import call_ban_address_search_api


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "data-sources": reverse("data-source-list", request=request),
            "places": reverse("place-list", request=request),
            # 'services': reverse('service-list', request=request, format=format)
        }
    )


class DataSourceList(APIView):
    """
    List all data sources.
    """

    @swagger_auto_schema(responses={200: DataSourceSerializer(many=True)})
    def get(self, request, format=None):
        data_sources = DataSource.objects.all()

        serializer = DataSourceSerializer(data_sources, many=True)
        return Response(serializer.data)


class PlaceList(APIView):
    """
    List all places, or create a new place.
    """

    @swagger_auto_schema(responses={200: PlaceSerializer(many=True)})
    def get(self, request, format=None):
        places = Place.objects.all()

        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=PlaceSerializer)
    # def post(self, request, format=None):
    #     serializer = PlaceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceDetail(APIView):
    """
    Retrieve, update or delete a place instance.
    """

    @swagger_auto_schema(responses={200: PlaceSerializer})
    def get(self, request, place_id, format=None):
        place = get_object_or_404(Place, pk=place_id)

        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=PlaceSerializer)
    # def put(self, request, place_id, format=None):
    #     place = get_object_or_404(Place, pk=place_id)
    #     serializer = PlaceSerializer(place, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, place_id, format=None):
    #     place = get_object_or_404(Place, pk=place_id)
    #     place.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class PlaceServiceList(APIView):
    """
    List all services of a place, or create a new service.
    """

    @swagger_auto_schema(responses={200: ServiceSerializer(many=True)})
    def get(self, request, place_id, format=None):
        place = get_object_or_404(Place, pk=place_id)
        services = place.services

        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=ServiceSerializer)
    # def post(self, request, place_id, format=None):
    #     place = get_object_or_404(Place, pk=place_id)
    #     serializer = ServiceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(place=place)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceServiceDetail(APIView):
    """
    Retrieve, update or delete a service instance.
    """

    @swagger_auto_schema(responses={200: ServiceSerializer})
    def get(self, request, place_id, service_id, format=None):
        place = get_object_or_404(Place, pk=place_id)
        service = get_object_or_404(place.services.all(), pk=service_id)

        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=ServiceSerializer)
    # def put(self, request, place_id, service_id, format=None):
    #     place = get_object_or_404(Place, pk=place_id)
    #     service = get_object_or_404(place.services.all(), pk=service_id)
    #     serializer = ServiceSerializer(service, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, place_id, service_id, format=None):
    #     place = get_object_or_404(Place, pk=place_id)
    #     service = get_object_or_404(place.services.all(), pk=service_id)
    #     service.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


address_search_q_param = openapi.Parameter(
    "q", openapi.IN_QUERY, description="address search query", type=openapi.TYPE_STRING
)


@swagger_auto_schema(method="get", manual_parameters=[address_search_q_param])
@api_view(["GET"])
def address_search(request):
    """
    https://adresse.data.gouv.fr/
    """
    results_json = call_ban_address_search_api(request.GET.get("q"))
    return Response(results_json)
