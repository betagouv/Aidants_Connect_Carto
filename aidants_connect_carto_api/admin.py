from django.contrib import admin

from aidants_connect_carto_api.models import Place, Service


class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "address_raw",
        "service_count",
        "created_at",
    )
    # list_filter = ("",)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "place",
        "support_access",
        "is_free",
        "created_at",
    )
    list_filter = ("place__name",)


admin.site.register(Place, PlaceAdmin)
admin.site.register(Service, ServiceAdmin)
