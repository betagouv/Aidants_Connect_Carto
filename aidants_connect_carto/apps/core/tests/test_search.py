from django.test import TestCase

from aidants_connect_carto.apps.core import search
from aidants_connect_carto.apps.core.models import DataSource, DataSet, Place, Service


class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        data_source_1 = DataSource.objects.create(name="Region Test", type="region")
        data_set_1 = DataSet.objects.create(
            name="Lieux EPN 2019", data_source=data_source_1
        )
        place_1 = Place.objects.create(
            name="Lieu Test 1",
            address_region_name="Auvergne-Rhône-Alpes",
            data_set_id=data_set_1.id,
        )
        Service.objects.create(name="Stockage numérique sécurisé", place_id=place_1.id)
        place_2 = Place.objects.create(
            name="Lieu Test 2",
            address_region_name="Île-de-France",
            data_set_id=data_set_1.id,
        )
        Service.objects.create(
            name="Accès à un équipement informatique", place_id=place_2.id
        )
        Service.objects.create(name="Stockage numérique sécurisé", place_id=place_2.id)
        Place.objects.create(name="another place", data_set_id=data_set_1.id)

    def test_search_form(self):
        search_query = {"name": "Lieu"}
        form = search.PlaceSearchForm(search_query)
        self.assertTrue(form.is_valid())

    def test_search_engine_query(self):
        engine = search.PlaceSearchEngine()
        self.assertRaises(TypeError, engine.search)
        self.assertRaises(AttributeError, engine.search, "name=Lieu")

        results = engine.search({})
        self.assertIsInstance(results, dict)

    def test_search_engine_clean_query(self):
        search_query = {"name": "Lieu", "type": "", "labels": []}
        engine = search.PlaceSearchEngine()
        search_query_cleaned = engine._clean_query(search_query)
        self.assertEqual(search_query_cleaned["name"], "Lieu")
        self.assertIn("labels", search_query_cleaned)
        self.assertNotIn("type", search_query_cleaned)

    def test_search_engine_results(self):
        search_query_1 = {}
        engine = search.PlaceSearchEngine()
        results = engine.search(search_query_1)
        self.assertFalse(results["has_filters"])
        self.assertEqual(len(results["current_filters"]), 0)
        self.assertEqual(results["places_total"], 3)

        search_query_1 = {"name": "Lieu", "type": ""}
        engine = search.PlaceSearchEngine()
        results = engine.search(search_query_1)
        self.assertTrue(results["has_filters"])
        self.assertEqual(len(results["current_filters"]), 1)
        self.assertEqual(results["places_total"], 2)
