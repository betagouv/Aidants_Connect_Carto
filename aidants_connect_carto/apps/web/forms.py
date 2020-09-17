from django import forms

from aidants_connect_carto import constants

from aidants_connect_carto.apps.core.models import Place, Service
from aidants_connect_carto.apps.core.forms import (
    # HorizontalRadioSelect,
    HorizontalCheckboxSelectMultiple,
)


class PlaceCreateForm(forms.ModelForm):
    """
    """

    target_audience = forms.TypedMultipleChoiceField(
        choices=constants.TARGET_AUDIENCE_CHOICES,
        widget=HorizontalCheckboxSelectMultiple(),
        help_text=Place._meta.get_field("target_audience").help_text,
    )

    def __init__(self, *args, **kwargs):
        super(PlaceCreateForm, self).__init__(*args, **kwargs)

        # set readonly fields
        for fieldname in Place.AUTO_POPULATED_FIELDS:
            self.fields[fieldname].widget.attrs["readonly"] = True

    class Meta:
        model = Place
        exclude = []
        # fields = ["address_raw", "address_housenumber"]


class ServiceCreateForm(forms.ModelForm):
    """
    """

    target_audience = forms.TypedMultipleChoiceField(
        choices=constants.TARGET_AUDIENCE_CHOICES,
        widget=HorizontalCheckboxSelectMultiple(),
        help_text=Service._meta.get_field("target_audience").help_text,
    )
    support_access = forms.TypedMultipleChoiceField(
        choices=constants.SUPPORT_ACCESS_CHOICES,
        widget=HorizontalCheckboxSelectMultiple(),
        help_text=Service._meta.get_field("support_access").help_text,
    )
    support_mode = forms.TypedMultipleChoiceField(
        choices=constants.SUPPORT_MODE_CHOICES,
        widget=HorizontalCheckboxSelectMultiple(),
        help_text=Service._meta.get_field("support_mode").help_text,
    )

    def __init__(self, *args, **kwargs):
        super(ServiceCreateForm, self).__init__(*args, **kwargs)

        # set readonly fields
        # for fieldname in Service.AUTO_POPULATED_FIELDS:
        #     self.fields[fieldname].widget.attrs["readonly"] = True

    class Meta:
        model = Service
        exclude = []
