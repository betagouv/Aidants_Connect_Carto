from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("aidants_connect_carto_api.urls")),
    path("", include("aidants_connect_carto_web.urls")),
]
