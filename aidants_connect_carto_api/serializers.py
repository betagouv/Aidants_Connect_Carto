from rest_framework import serializers
# from drf_braces.forms.serializer_form import SerializerForm

from aidants_connect_carto_api.models import Place, Service


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = [
            "id", "name",
            "address_raw", "address_housenumber", "address_street", "address_postcode", "address_citycode", "address_city",
            "latitude", "longitude", "is_itinerant",
            "contact_email", "contact_phone", "contact_website",
            "opening_hours_raw",
            "has_equipment_wifi", "has_equipment_computer", "has_equipment_scanner", "has_equipment_printer", "equipment_other",
            "has_accessibility_hi", "has_accessibility_mi", "has_accessibility_pi", "has_accessibility_vi",
            "languages",
            "payment_methods",
            "osm_node_id",
            "created_at", "updated_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id", "name", "description", "place_id", "siret",
            "public_target", "support_mode",
            "schedule_hours_raw",
            "is_free", "price_detail", "payment_methods",
            "has_label_aidants_connect", "has_label_mfs", "label_other",
            "created_at", "updated_at",
        ]
