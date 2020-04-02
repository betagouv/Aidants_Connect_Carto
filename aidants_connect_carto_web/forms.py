from django import forms

from aidants_connect_carto_api.models import Place, Service
from aidants_connect_carto_api.serializers import PlaceSerializer


class PlaceCreateForm(forms.ModelForm):
    """
    """
    def __init__(self, *args, **kwargs):
        super(PlaceCreateForm, self).__init__(*args, **kwargs)
        # set help_text as label
        for fieldname in self.fields:
            # self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].help_text
            self.fields[fieldname].label = self.fields[fieldname].help_text
            self.fields[fieldname].help_text = None
        # set readonly fields
        for fieldname in Place.FORM_READONLY_FIELDS:
            self.fields[fieldname].widget.attrs['readonly'] = True

    class Meta:
        model = Place
        exclude = []
        # fields = ["address_raw", "address_housenumber"]
