from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core.models import Place, Service, DataSource
from aidants_connect_carto.apps.core.search import PlaceSearchEngine, PlaceSearchForm
from aidants_connect_carto.apps.core.stats import get_model_stats
from aidants_connect_carto.apps.web.forms import PlaceCreateForm, ServiceCreateForm


def home_page(request):
    form = PlaceSearchForm(request.GET)
    return render(request, "home_page.html", {"search_form": form})


def places_list(request):
    form = PlaceSearchForm(request.GET)
    engine = PlaceSearchEngine()
    results = engine.search(query=request.GET)

    return render(
        request,
        "places/places_list.html",
        {"search_form": form, "search_results": results},
    )


def place_details(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place_services = place.services.all().order_by("id")
    return render(
        request,
        "places/place_details.html",
        {"place": place, "place_services": place_services},
    )


def place_create(request):
    if request.method == "GET":
        form = PlaceCreateForm()

    else:
        form = PlaceCreateForm(request.POST)

        if form.is_valid():
            place = form.save()
            messages.success(
                request,
                f"Le lieu <strong>{place.name}</strong> a été créé avec succès !",
            )
            return redirect("place_details", place_id=place.id)

    return render(
        request, "places/place_create.html", {"form": form, "action": "create"}
    )


def place_update(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    if request.method == "GET":
        form = PlaceCreateForm(instance=place)

    else:
        form = PlaceCreateForm(request.POST, instance=place)

        if form.is_valid():
            place = form.save()
            messages.success(
                request,
                f"Le lieu <strong>{place.name}</strong> a été modifié avec succès !",
            )
            return redirect("place_details", place_id=place.id)

    return render(
        request,
        "places/place_create.html",
        {"form": form, "action": "update", "place_id": place_id},
    )


def service_create(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    if request.method == "GET":
        form = ServiceCreateForm()

    else:
        form = ServiceCreateForm(request.POST)

        if form.is_valid():
            service = form.save()
            messages.success(
                request,
                f"Le service <strong>{service.name}</strong> a été créé avec succès !",
            )
            return redirect("place_details", place_id=service.place_id)

    return render(
        request,
        "places/services/service_create.html",
        {"form": form, "action": "create", "place": place},
    )


def service_update(request, place_id, service_id):
    place = get_object_or_404(Place, pk=place_id)
    service = get_object_or_404(place.services.all(), pk=service_id)
    if request.method == "GET":
        form = ServiceCreateForm(instance=service)

    else:
        form = ServiceCreateForm(request.POST, instance=service)

        if form.is_valid():
            service = form.save()
            messages.success(
                request,
                f"Le service <strong>{service.name}</strong> a été modifié avec succès !",  # noqa
            )
            return redirect("place_details", place_id=service.place_id)

    return render(
        request,
        "places/services/service_create.html",
        {"form": form, "action": "update", "place": place, "service_id": service_id},
    )


def data_sources_list(request):
    data_sources = DataSource.objects.select_related().all()
    data_sources_count = data_sources.count()
    data_sources_national = data_sources.filter(
        type=constants.DATA_SOURCE_TYPE_NATIONAL
    )
    data_sources_hub = data_sources.filter(type=constants.DATA_SOURCE_TYPE_HUB)
    data_sources_region = data_sources.filter(type=constants.DATA_SOURCE_TYPE_REGION)
    data_sources_departement = data_sources.filter(
        type=constants.DATA_SOURCE_TYPE_DEPARTEMENT
    )

    return render(
        request,
        "data_sources_list.html",
        {
            "data_sources_count": data_sources_count,
            "data_sources_national": data_sources_national,
            "data_sources_hub": data_sources_hub,
            "data_sources_region": data_sources_region,
            "data_sources_departement": data_sources_departement,
        },
    )


def stats(request):
    model_stats = get_model_stats()

    import json
    import pandas as pd
    import numpy as np

    # region geojson
    with open("data/geo/regions-version-simplifiee.geojson", "r") as f:
        region_geojson = json.load(f)
        for index, region in enumerate(region_geojson["features"]):
            region_geojson["features"][index]["properties"]["place_count"] = next(
                (
                    region_agg["place_count"]
                    for region_agg in model_stats[
                        "place_address_region_name_aggregation"
                    ]
                    if region_agg["address_region_name"] == region["properties"]["nom"]
                ),
                0,
            )

    # place fields fill stats
    place_df = pd.DataFrame.from_records(Place.objects.all().values())
    place_df = (
        place_df.replace("", np.nan)
        .replace([], np.nan)
        .replace(constants.CHOICE_OTHER, np.nan)
    )
    place_fields_fill_count_df = place_df.count()

    # service fields fill stats
    service_df = pd.DataFrame.from_records(Service.objects.all().values())
    service_df = (
        service_df.replace("", np.nan)
        .replace(constants.CHOICE_OTHER, np.nan)
        .replace([], np.nan)
    )
    service_fields_fill_count_df = service_df.count()

    return render(
        request,
        "stats.html",
        {
            **model_stats,
            "region_geojson": json.dumps(region_geojson),
            "place_field_fill": [
                {
                    "name": "Adresse",
                    "fill_stats": [
                        {"key": key, "value": place_fields_fill_count_df[key]}
                        for key in [
                            "address_raw",
                            "address_housenumber",
                            "address_street",
                            "address_postcode",
                            "address_city",
                            "address_departement_name",
                            "address_region_name",
                            "latitude",
                            "longitude",
                        ]
                    ],
                },
                {
                    "name": "Contact",
                    "fill_stats": [
                        {"key": key, "value": place_fields_fill_count_df[key]}
                        for key in [
                            "contact_phone_raw",
                            "contact_phone",
                            "contact_email",
                            "contact_website_url",
                            "contact_facebook_url",
                            "contact_twitter_url",
                            "contact_youtube_url",
                        ]
                    ],
                },
                {
                    "name": "Horaires",
                    "fill_stats": [
                        {
                            "key": key,
                            "value": place_fields_fill_count_df[key]
                            if (key in place_fields_fill_count_df)
                            else 0,
                        }
                        for key in ["opening_hours_raw", "opening_hours_osm_format"]
                    ],
                },
                {
                    "name": "Public cible",
                    "fill_stats": [
                        {
                            "key": key,
                            "value": place_fields_fill_count_df[key]
                            if (key in place_fields_fill_count_df)
                            else 0,
                        }
                        for key in ["target_audience_raw", "target_audience"]
                    ],
                },
                {
                    "name": "autres",
                    "fill_stats": [
                        {
                            "key": key,
                            "value": place_fields_fill_count_df[key]
                            if (key in place_fields_fill_count_df)
                            else 0,
                        }
                        for key in [
                            "supporting_structure_name",
                            "type",
                            "status",
                            "legal_entity_type",
                            "siret",
                            "is_itinerant",
                            "is_online",
                            "languages",
                            "payment_methods",
                            "osm_node_id",
                        ]
                    ],
                },
            ],
            "service_field_fill": [
                {
                    "name": "Horaires",
                    "fill_stats": [
                        {
                            "key": key,
                            "value": service_fields_fill_count_df[key]
                            if (key in service_fields_fill_count_df)
                            else 0,
                        }
                        for key in ["schedule_hours_raw", "schedule_hours_osm_format"]
                    ],
                },
                {
                    "name": "Accompagnement",
                    "fill_stats": [
                        {
                            "key": key,
                            "value": service_fields_fill_count_df[key]
                            if (key in service_fields_fill_count_df)
                            else 0,
                        }
                        for key in ["target_audience", "support_access", "support_mode"]
                    ],
                },
                {
                    "name": "autres",
                    "fill_stats": [
                        {
                            "key": key,
                            "value": service_fields_fill_count_df[key]
                            if (key in service_fields_fill_count_df)
                            else 0,
                        }
                        for key in [
                            "siret",
                            "price_details",
                            "payment_methods",
                            "label_other",
                        ]
                    ],
                },
            ],
        },
    )
