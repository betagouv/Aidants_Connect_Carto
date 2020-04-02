from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from aidants_connect_carto_api.models import Place
from aidants_connect_carto_web.forms import PlaceCreateForm


def home_page(request):
    return render(request, "home_page.html")

def place_list(request):
    places = Place.objects.all()
    return render(request, "places/place_list.html", { "places": places })

def place_details(request, pk):
    place = get_object_or_404(Place, pk=pk)
    return render(request, "places/place_details.html", { "place": place })

def place_create(request):
    if request.method == "GET":
        form = PlaceCreateForm()
        return render(request, "places/place_create.html", { "form": form })
    
    else:
        form = PlaceCreateForm(request.POST)

        if form.is_valid():
            # data = form.cleaned_data
            # place = Place.objects.create(data)
            place = form.save()
            messages.success(request, "Le lieu a été créé avec succès !")
            return redirect("place_details", pk=place.id)
        else:
            return render(request, "places/place_create.html", { "form": form })
