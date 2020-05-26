from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator

from aidants_connect_carto import constants

from aidants_connect_carto.apps.core.models import Place, Service


class PlaceSearchForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Le nom d'un lieu ou d'une ville",
                "autofocus": "autofocus",
            }
        )
    )

    service_name = forms.ChoiceField(
        choices=zip(constants.SERVICE_NAME_LIST, constants.SERVICE_NAME_LIST),
        widget=forms.Select(),
    )
    opening_hours = forms.ChoiceField(
        choices=[("open", "Ouvert en ce moment")], widget=forms.Select(),
    )
    is_online = forms.ChoiceField(
        choices=[("hide", "Cacher"), ("only", "Uniquement")], widget=forms.Select(),
    )
    service_label_aidants_connect = forms.BooleanField(
        label=Service._meta.get_field("has_label_aidants_connect").verbose_name,
        initial=False,
    )

    ADD_EMPTY_CHOICE_FIELDS = [
        "type",
        "opening_hours",
        "is_online",
        "service_name",
    ]

    class Meta:
        model = Place
        fields = [
            "name",
            "type",
            "opening_hours",
            "address_departement_name",
            "address_region_name",
            # "has_equipment_wifi",
            # "has_equipment_computer",
            # "has_equipment_scanner",
            # "has_equipment_printer",
            "service_name",
            "has_label_fs",
            "service_label_aidants_connect",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # No field is required for a search to be launched.
        for field_name in self.fields:
            self.fields[field_name].required = False

        # We must add an "empty" value for some fields
        # so we can search without specifying a value.
        for field_name in self.ADD_EMPTY_CHOICE_FIELDS:
            field = self.fields[field_name]
            field.choices = [("", "Tous")] + field.choices
            field.initial = ""


class PlaceSearchEngine:
    def __init__(self, *args, **kwargs):

        # This is a good place to initialize a few settings...
        self.DEFAULT_ORDER_BY = "name"
        self.RESULTS_PER_PAGE = kwargs.get(
            "RESULTS_PER_PAGE", settings.SEARCH_RESULTS_PER_PAGE
        )

    def search(self, query):
        """
        Execute the specified `query` and return the results as a `dict`.
        The `query` itself is passed as a `dict`, or possibly directly
        the Django `QueryDict from an incoming HTTP request.`
        Returns an object with 2 keys: 'places_page' and 'places_total'
        """
        # clean incoming query
        self.query = self._clean_query(query)

        # build queryset
        self.queryset = self._build_queryset()

        # build results
        self.results = self._build_results()

        return self.results

    def _clean_query(self, query):
        """
        Clean the incoming query
        - remove keys with empty string
        (TODO: clean empty keys in the frontend on submit ?)
        """
        cleaned_query = dict()

        for (key, value) in query.items():
            if value != "":
                cleaned_query[key] = value

        return cleaned_query

    def _build_queryset(self):
        """
        Progressively build, and then return, the relevant Django ORM queryset
        by analyzing the specified query.
        """

        # We start with all the objects.
        qs = Place.objects.all()

        # And then, little by little, we narrow the search down.
        if self.query.get("name"):
            # qs = qs.filter(name__icontains=self.query.get("name"))
            qs = qs.annotate(
                search=SearchVector("name") + SearchVector("address_city")
            ).filter(search=self.query.get("name"))

        if self.query.get("type"):
            qs = qs.filter(type=self.query.get("type"))

        if self.query.get("is_online"):
            is_online_filter_value = (
                True if (self.query.get("is_online") == "uniquement") else False
            )
            qs = qs.filter(is_online=is_online_filter_value)

        if self.query.get("address_departement_name"):
            qs = qs.filter(
                address_departement_name=self.query.get("address_departement_name")
            )
        if self.query.get("address_region_name"):
            qs = qs.filter(address_region_name=self.query.get("address_region_name"))

        # if self.query.get("has_equipment_wifi"):
        #     qs = qs.filter(has_equipment_wifi=True)
        # if self.query.get("has_equipment_computer"):
        #     qs = qs.filter(has_equipment_computer=True)
        # if self.query.get("has_equipment_scanner"):
        #     qs = qs.filter(has_equipment_scanner=True)
        # if self.query.get("has_equipment_printer"):
        #     qs = qs.filter(has_equipment_printer=True)

        if self.query.get("service_name"):
            qs = qs.filter(services__name=self.query.get("service_name"))

        if self.query.get("has_label_fs"):
            qs = qs.filter(has_label_fs=True)
        if self.query.get("service_label_aidants_connect"):
            qs = qs.filter(services__has_label_aidants_connect=True)

        return qs  # Note: at this point, the database query has not been executed yet.

    def _build_results(self):
        """
        Execute the database query and build the results to be returned
        to the calling code, typically as a more or less complex `dict`, which
        could also contain meta-information about the search, like the total
        number of results, ...
        - order_by
        - opening_hours
        - pagination
        - current filters
        """
        # order_by
        order_by_field = self.query.get("order_by", self.DEFAULT_ORDER_BY)
        self.queryset = self.queryset.order_by(order_by_field)

        raw_results = self.queryset

        # opening_hours (place.is_open) filter
        if self.query.get("opening_hours"):
            raw_results = [place for place in raw_results if place.is_open]

        # paginator <-- db query is executed here!
        paginator = Paginator(raw_results, self.RESULTS_PER_PAGE)
        page_number = self.query.get("page", 1)
        page_obj = paginator.get_page(page_number)

        # current filters
        current_filters_list = []
        for (key, value) in self.query.items():
            current_filters_list.append(
                {
                    "type": key,
                    "value": value,
                    "url_parameters_with_filter_removed": "&".join(
                        [f"{k}={v}" for k, v in self.query.items() if k != key]
                    ),
                }
            )

        return {
            "has_filters": bool(self.query),
            "current_filters": current_filters_list,
            "places_page": page_obj,
            "places_total": paginator.count,
        }
