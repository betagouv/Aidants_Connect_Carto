from django.forms import ModelForm

from aidants_connect_carto_api.models import Place


class PlaceSearchForm(ModelForm):
    class Meta:
        model = Place
        fields = [
            "name",
            "type",
            "has_equipment_wifi",
            "has_equipment_computer",
            "has_equipment_scanner",
            "has_equipment_printer",
        ]
