from django import forms

from aidants_connect_carto_api.models import Place, Service
from aidants_connect_carto_api import constants


class HorizontalRadioSelect(forms.RadioSelect):
    template_name = "partials/forms/widgets/multiple_input_horizontal.html"


class HorizontalCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "partials/forms/widgets/multiple_input_horizontal.html"


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
    support_access = forms.ChoiceField(
        choices=constants.SERVICE_SUPPORT_ACCESS_CHOICES,
        widget=HorizontalRadioSelect(),
        help_text=Service._meta.get_field("support_access").help_text,
    )
    support_mode = forms.ChoiceField(
        choices=constants.SERVICE_SUPPORT_MODE_CHOICES,
        widget=HorizontalRadioSelect(),
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
