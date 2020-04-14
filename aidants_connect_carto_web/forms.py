from django import forms

from aidants_connect_carto_api.models import Place, Service


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
            self.fields[fieldname].label = self.fields[fieldname].help_text
            self.fields[fieldname].help_text = None

        # set readonly fields
        for fieldname in Place.FORM_READONLY_FIELDS:
            self.fields[fieldname].widget.attrs["readonly"] = True

    class Meta:
        model = Place
        exclude = []
        # fields = ["address_raw", "address_housenumber"]


class ServiceCreateForm(forms.ModelForm):
    """
    """

    public_target = forms.TypedMultipleChoiceField(
        choices=Service.PUBLIC_CHOICES,
        widget=HorizontalCheckboxSelectMultiple(),
        help_text=Service._meta.get_field("public_target").help_text,
    )
    support_access = forms.ChoiceField(
        choices=Service.SUPPORT_ACCESS_CHOICES,
        widget=HorizontalRadioSelect(),
        help_text=Service._meta.get_field("support_access").help_text,
    )
    support_mode = forms.ChoiceField(
        choices=Service.SUPPORT_MODE_CHOICES,
        widget=HorizontalRadioSelect(),
        help_text=Service._meta.get_field("support_mode").help_text,
    )

    def __init__(self, *args, **kwargs):
        super(ServiceCreateForm, self).__init__(*args, **kwargs)

        # set help_text as label
        for fieldname in self.fields:
            self.fields[fieldname].label = self.fields[fieldname].help_text
            self.fields[fieldname].help_text = None

        # set readonly fields
        # for fieldname in Service.FORM_READONLY_FIELDS:
        #     self.fields[fieldname].widget.attrs["readonly"] = True

    class Meta:
        model = Service
        exclude = []
