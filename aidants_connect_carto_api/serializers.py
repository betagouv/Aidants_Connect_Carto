from rest_framework import serializers
# from drf_braces.forms.serializer_form import SerializerForm

from aidants_connect_carto_api.models import Place, Service


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = [
            "id", "name",
            "address_raw", "address_housenumber", "address_street", "address_postcode", "address_citycode", "address_city",
            "latitude", "longitude", "itinerant",
            "contact_email", "contact_phone", "contact_website",
            "opening_hours_raw",
            "payment_methods",
            "accessibility_hi", "accessibility_mi", "accessibility_pi", "accessibility_vi",
            "languages",
            "equipement_wifi", "equipement_computer", "equipement_scanner", "equipement_printer", "equipement_other",
            "osm_node_id",
            "created_at", "updated_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id", "description", "place_id", "siret",
            "public_target", "support_mode",
            "schedule_hours_raw",
            "price_free", "price_detail", "payment_methods",
            "label_aidants_connect", "label_mfs", "label_other",
            "created_at", "updated_at",
        ]
