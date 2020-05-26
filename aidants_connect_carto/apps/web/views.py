from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core.models import Place, DataSource
from aidants_connect_carto.apps.core.search import PlaceSearchEngine, PlaceSearchForm
from aidants_connect_carto.apps.web.forms import PlaceCreateForm, ServiceCreateForm


def home_page(request):
    return render(request, "home_page.html")


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
    data_sources = DataSource.objects.all()  # .order_by("name")

    return render(request, "data_sources_list.html", {"data_sources": data_sources},)


def stats(request):
    data_source_count = DataSource.objects.count()
    place_count = Place.objects.count()
    place_with_service_count = Place.objects.exclude(services__isnull=True).count()
    service_name_aggregation = []
    for service_name in constants.SERVICE_NAME_LIST:
        service_name_aggregation.append(
            {
                "service_name": service_name,
                "place_count": Place.objects.filter(
                    services__name=service_name
                ).count(),
            }
        )
    service_name_aggregation.sort(key=lambda x: x["place_count"], reverse=True)

    return render(
        request,
        "stats.html",
        {
            "data_source_count": data_source_count,
            "place_count": place_count,
            "place_with_service_count": place_with_service_count,
            "service_name_aggregation": service_name_aggregation,
        },
    )
