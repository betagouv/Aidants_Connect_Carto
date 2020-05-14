from django.db.models import Count

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core.models import Place, Service, DataSource


def get_data_source_model_stats():
    data_source_count = DataSource.objects.count()
    return {"data_source_count": data_source_count}


def get_place_model_stats():
    place_count = Place.objects.count()
    place_with_service_count = Place.objects.exclude(services__isnull=True).count()

    place_address_region_name_aggregation = (
        Place.objects.exclude(address_region_name="")
        .values("address_region_name")
        .annotate(place_count=Count("id"))
        .order_by("address_region_name")
    )

    return {
        "place_count": place_count,
        "place_with_service_count": place_with_service_count,
        "place_address_region_name_aggregation": place_address_region_name_aggregation,
    }


def get_service_model_stats():
    service_count = Service.objects.count()

    service_name_aggregation = []
    for service_name in constants.SERVICE_NAME_LIST:
        service_name_aggregation.append(
            {
                "name": service_name,
                "place_count": Place.objects.filter(
                    services__name=service_name
                ).count(),
            }
        )
    service_name_aggregation.sort(key=lambda x: x["place_count"], reverse=True)

    return {
        "service_count": service_count,
        "service_name_aggregation": service_name_aggregation,
    }


def get_model_stats():
    """
    Helper method to group all the model stats in the same dict
    """
    return {
        **get_data_source_model_stats(),
        **get_place_model_stats(),
        **get_service_model_stats(),
    }
