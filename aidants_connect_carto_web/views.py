from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from aidants_connect_carto_api.models import Place
from aidants_connect_carto_web.forms import PlaceCreateForm, ServiceCreateForm


def home_page(request):
    return render(request, "home_page.html")


def place_list(request):
    places = Place.objects.all()
    return render(request, "places/place_list.html", { "places": places })

def place_details(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    place_services = place.services.all().order_by('id')
    print(place.id)
    print(place.services)
    return render(request, "places/place_details.html", { "place": place, "place_services": place_services })

def place_create(request):
    if request.method == "GET":
        form = PlaceCreateForm()
        return render(request, "places/place_create.html", { "form": form })
    
    else:
        form = PlaceCreateForm(request.POST)

        if form.is_valid():
            place = form.save()
            messages.success(request, f"Le lieu <strong>{place.name}</strong> a été créé avec succès !")
            return redirect("place_details", place_id=place.id)
        else:
            return render(request, "places/place_create.html", { "form": form })


def service_create(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    if request.method == "GET":
        form = ServiceCreateForm()
        return render(request, "places/services/service_create.html", { "place": place, "form": form })
    
    else:
        form = ServiceCreateForm(request.POST)

        if form.is_valid():
            service = form.save()
            messages.success(request, f"Le service <strong>{service.name}</strong> a été créé avec succès !")
            return redirect("place_details", place_id=service.place_id)
        else:
            return render(request, "places/services/service_create.html", { "place": place, "form": form })