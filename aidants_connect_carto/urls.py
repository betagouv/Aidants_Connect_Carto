from django.contrib import admin
from django.urls import path, include

# from aidants_connect_carto import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("aidants_connect_carto_api.urls")),
]
