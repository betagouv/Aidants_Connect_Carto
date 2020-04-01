from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from aidants_connect_carto_api import views


urlpatterns = [
    path("", views.api_root),
    path("places/", views.PlaceList.as_view(), name="place-list"),
    path("places/<int:pk>", views.PlaceDetail.as_view(), name="place-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
