from django.conf import settings
from django.forms import ModelForm

from aidants_connect_carto.apps.core.models import Place


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # No field is required for a search to be launched.
        for field_name in self.fields:
            self.fields[field_name].required = False

        # We must add an "empty" value for the `type` field
        # so we can search without specifying one.
        type_field = self.fields["type"]
        type_field.choices = [("", "")] + type_field.choices
        type_field.initial = ""


class PlaceSearchEngine:

    TARGET_CLASS = Place  # The type of object this search engine works on

    def __init__(self, *args, **kwargs):

        # This is a good place to initialize a few settings...
        self.RESULTS_PER_PAGE = kwargs.get(
            "RESULTS_PER_PAGE", settings.SEARCH_RESULTS_PER_PAGE
        )

    def search(self, query):
        """Execute the specified `query` and return the results as a `dict`.
        The `query` itself is passed as a `dict`, or possibly directly
        the Django `QueryDict from an incoming HTTP request.`
        """
        self.query = query.copy()
        self.queryset = self._build_queryset()
        self.results = self._build_results()

        return self.results

    def _build_queryset(self):
        """Progressively build, and then return, the relevant Django ORM queryset
        by analyzing the specified query.
        """
        query = self.query

        # We start with all the objects.
        qs = self.TARGET_CLASS.objects.all()

        # And then, little by little, we narrow the search down.
        if "name" in query:
            qs = qs.filter(name__icontains=query.get("name"))

        if "type" in query:
            searched_type = query.get("type")
            if searched_type != "":
                qs = qs.filter(type=query.get("type"))

        if "has_equipment_wifi" in query:
            qs = qs.filter(has_equipment_wifi=True)

        if "has_equipment_computer" in query:
            qs = qs.filter(has_equipment_computer=True)

        if "has_equipment_scanner" in query:
            qs = qs.filter(has_equipment_scanner=True)

        if "has_equipment_printer" in query:
            qs = qs.filter(has_equipment_printer=True)

        # And so on... But some will be trickier to implement ;)

        return qs  # Note: at this point, the database query has not been executed yet.

    def _build_results(self):
        """Execute the database query and build the results to be returned
        to the calling code, typically as a more or less complex `dict`, which
        could also contain meta-information about the search, like the total
        number of results, ...
        """
        page_number = self.query.get("page", 1)
        offset = self.RESULTS_PER_PAGE * (page_number - 1)

        raw_results = self.queryset[
            offset : offset + self.RESULTS_PER_PAGE
        ]  # <-- db query is executed here!

        # We could now build a refined representation of our results,
        # but right now this is merely a proof of concept, so we just...

        return raw_results
