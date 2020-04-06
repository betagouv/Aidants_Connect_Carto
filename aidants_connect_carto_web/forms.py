from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from aidants_connect_carto_api.models import Place, Service
# from aidants_connect_carto_api.serializers import PlaceSerializer, ServiceSerialier


class HorizontalRadioSelect(forms.RadioSelect):
    template_name = "partials/forms/widgets/multiple_input_horizontal.html"

class HorizontalCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "partials/forms/widgets/multiple_input_horizontal.html"


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


class ServiceCreateForm(forms.ModelForm):
    """
    """
    support_mode = forms.ChoiceField(
        choices=Service.SUPPORT_CHOICES,
        widget=HorizontalRadioSelect(),
        help_text=Service._meta.get_field('support_mode').help_text
    )
    public_target = forms.TypedMultipleChoiceField(
        choices=Service.PUBLIC_CHOICES,
        widget=HorizontalCheckboxSelectMultiple(),
        help_text=Service._meta.get_field('public_target').help_text
    )

    def __init__(self, *args, **kwargs):
        super(ServiceCreateForm, self).__init__(*args, **kwargs)
        # set help_text as label
        for fieldname in self.fields:
            self.fields[fieldname].label = self.fields[fieldname].help_text
            self.fields[fieldname].help_text = None
        # set readonly fields
        for fieldname in Service.FORM_READONLY_FIELDS:
            self.fields[fieldname].widget.attrs['readonly'] = True


    class Meta:
        model = Service
        exclude = []
