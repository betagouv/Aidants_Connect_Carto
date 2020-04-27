from rest_framework import serializers

# from drf_braces.forms.serializer_form import SerializerForm

from aidants_connect_carto.apps.core.models import Place, Service


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "name",
            "supporting_structure_name",
            "description",
            "type",
            "status",
            "legal_entity_type",
            "address_raw",
            "address_housenumber",
            "address_street",
            "address_postcode",
            "address_citycode",
            "address_city",
            "address_departement_code",
            "address_departement_name",
            "address_region_name",
            "latitude",
            "longitude",
            "is_itinerant",
            "itinerant_details",
            "is_online",
            "contact_email",
            "contact_phone_raw",
            "contact_phone",
            "contact_phone_details",
            "contact_website_url",
            "contact_facebook_url",
            "contact_twitter_url",
            "contact_youtube_url",
            "opening_hours_raw",
            "opening_hours_osm_format",
            "has_equipment_wifi",
            "has_equipment_computer",
            "has_equipment_scanner",
            "has_equipment_printer",
            "equipment_other",
            "has_accessibility_hi",
            "has_accessibility_mi",
            "has_accessibility_pi",
            "has_accessibility_vi",
            "languages",
            "target_audience_raw",
            "target_audience",
            "payment_methods",
            "osm_node_id",
            "created_at",
            "updated_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "description",
            "place_id",
            "siret",
            "target_audience",
            "support_access",
            "support_mode",
            "schedule_hours_raw",
            "schedule_hours_osm_format",
            "is_free",
            "price_details",
            "payment_methods",
            "has_label_aidants_connect",
            "has_label_mfs",
            "label_other",
            "created_at",
            "updated_at",
        ]
