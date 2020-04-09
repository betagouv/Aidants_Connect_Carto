from django.urls import path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# from rest_framework.urlpatterns import format_suffix_patterns

from aidants_connect_carto_api import views


schema_view = get_schema_view(
    openapi.Info(
        title="Aidants Connect Carto API",
        default_version="v1",
        description="description",
    ),
)


urlpatterns = [
    path("", views.api_root),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("places/", views.PlaceList.as_view(), name="place-list"),
    path("places/<int:pk>/", views.PlaceDetail.as_view(), name="place-detail"),
    path("address/search", views.address_search, name="address-search"),
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])
