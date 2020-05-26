from django.contrib import admin

from aidants_connect_carto.apps.core.models import DataSource, Place, Service
from aidants_connect_carto.apps.web.forms import PlaceCreateForm, ServiceCreateForm


class DataSourceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "dataset_name",
        "place_count",
        "dataset_last_updated",
        "created_at",
    )
    ordering = ("name",)
    list_filter = ("type",)


class PlaceAdmin(admin.ModelAdmin):
    # to beautify the display of ArrayField fields
    form = PlaceCreateForm

    list_display = (
        "id",
        "name",
        "address_raw",
        "data_source",
        "service_count",
        "created_at",
    )
    ordering = ("id",)
    list_filter = (
        "data_source__name",
        "address_region_name",
        "address_departement_name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceCreateForm

    list_display = (
        "id",
        "name",
        "place",
        "support_access",
        "is_free",
        "created_at",
    )
    ordering = ("id",)
    list_filter = ("place__name",)


admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Service, ServiceAdmin)
