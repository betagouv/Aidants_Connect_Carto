from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

from aidants_connect_carto.apps.core.models import Place
from aidants_connect_carto.apps.core.search import PlaceSearchEngine, PlaceSearchForm
from aidants_connect_carto.apps.web.forms import PlaceCreateForm, ServiceCreateForm


def home_page(request):
    return render(request, "home_page.html")


# def places_list(request):
#     places = Place.objects.all().order_by("name")

#     services = list(
#         places.order_by().values_list("services__name", flat="True").distinct()
#     )
#     services = list(filter(None, services))
#     services.sort()


#     return render(
#         request,
#         "places/places_list.html",
#         {
#             "places_page": page_obj,
#             "places_total": paginator.count,
#             "place_types": constants.PLACE_TYPE_CHOICES,
#             "services": services,
#         },
#     )


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
