from django.urls import path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# from rest_framework.urlpatterns import format_suffix_patterns

from aidants_connect_carto.apps.api import views


schema_view = get_schema_view(
    openapi.Info(
        title="Aidants Connect Carto API",
        default_version="v1",
        description="description",
    ),
)

app_name = "api"
urlpatterns = [
    path("", views.api_root, name="root"),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("data-sources/", views.DataSourceList.as_view(), name="data-source-list"),
    path(
        "data-sources/<int:data_source_id>/",
        views.DataSourceDetail.as_view(),
        name="data-source-detail",
    ),
    path("places/", views.PlaceList.as_view(), name="place-list"),
    path("places/<int:place_id>/", views.PlaceDetail.as_view(), name="place-detail"),
    path(
        "places/<int:place_id>/services/",
        views.PlaceServiceList.as_view(),
        name="place-service-list",
    ),
    path(
        "places/<int:place_id>/services/<int:service_id>/",
        views.PlaceServiceDetail.as_view(),
        name="place-service-detail",
    ),
    path("stats", views.stats, name="stats"),
    path("address/search", views.address_search, name="address-search"),
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])
