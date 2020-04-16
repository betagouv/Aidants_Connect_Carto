from django.contrib import admin

from aidants_connect_carto.apps.core.models import Place, Service
from aidants_connect_carto.apps.web.forms import PlaceCreateForm, ServiceCreateForm


class PlaceAdmin(admin.ModelAdmin):

    # to beautify the display of ArrayField fields
    form = PlaceCreateForm

    list_display = (
        "id",
        "name",
        "address_raw",
        "service_count",
        "created_at",
    )
    list_filter = ("address_region_name",)


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
    list_filter = ("place__name",)


admin.site.register(Place, PlaceAdmin)
admin.site.register(Service, ServiceAdmin)
