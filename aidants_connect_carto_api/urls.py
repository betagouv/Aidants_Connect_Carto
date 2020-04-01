from django.urls import path

from aidants_connect_carto_api import views


urlpatterns = [
    # path('', views.api_home),
    path('places/', views.place_list),
    path('places/<int:pk>', views.place_detail),
]
