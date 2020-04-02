from django.urls import path

from aidants_connect_carto_web import views


urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("lieux", views.place_list, name="place_list"),
    path("lieux/<int:pk>", views.place_details, name="place_details"),
    path("lieux/nouveau", views.place_create, name="place_create"),
]
