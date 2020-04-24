from django import forms


class HorizontalRadioSelect(forms.RadioSelect):
    template_name = "partials/forms/widgets/multiple_input_horizontal.html"


class HorizontalCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "partials/forms/widgets/multiple_input_horizontal.html"
