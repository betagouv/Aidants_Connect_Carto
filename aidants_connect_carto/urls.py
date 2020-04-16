from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("aidants_connect_carto.apps.api.urls")),
    path("", include("aidants_connect_carto.apps.web.urls")),
]
