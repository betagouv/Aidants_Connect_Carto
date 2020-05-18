from django.test import TestCase

from aidants_connect_carto.apps.core import stats
from aidants_connect_carto.apps.core.models import DataSource, Place, Service


class DataSourceModelStatsTestCase(TestCase):
    def setUp(self):
        DataSource.objects.create(
            name="Region Test", type="region", dataset_name="Lieux EPN 2019"
        )

    def test_data_source_model_stats(self):
        data_source_stats = stats.get_data_source_model_stats()
        self.assertTrue(isinstance(data_source_stats, dict))
        self.assertEqual(data_source_stats["data_source_count"], 1)


class PlaceModelStatsTestCase(TestCase):
    def setUp(self):
        place_1 = Place.objects.create(
            name="Lieu Test 1", address_region_name="Auvergne-Rhône-Alpes"
        )
        Service.objects.create(
            name="Accès à un équipement informatique", place_id=place_1.id
        )
        Place.objects.create(name="Lieu Test 2", address_region_name="Île-de-France")
        Place.objects.create(name="Lieu Test 3", address_region_name="Île-de-France")

    def test_place_model_stats(self):
        place_stats = stats.get_place_model_stats()
        self.assertTrue(isinstance(place_stats, dict))
        self.assertEqual(place_stats["place_count"], 3)
        self.assertEqual(place_stats["place_with_service_count"], 1)
        self.assertEqual(len(place_stats["place_address_region_name_aggregation"]), 2)
        self.assertEqual(
            place_stats["place_address_region_name_aggregation"][0][
                "address_region_name"
            ],
            "Auvergne-Rhône-Alpes",
        )


class ServiceModelStatsTestCase(TestCase):
    def setUp(self):
        place_1 = Place.objects.create(
            name="Lieu Test 1", address_region_name="Auvergne-Rhône-Alpes"
        )
        Service.objects.create(name="Stockage numérique sécurisé", place_id=place_1.id)
        place_2 = Place.objects.create(
            name="Lieu Test 2", address_region_name="Île-de-France"
        )
        Service.objects.create(
            name="Accès à un équipement informatique", place_id=place_2.id
        )
        Service.objects.create(name="Stockage numérique sécurisé", place_id=place_2.id)

    def test_service_model_stats(self):
        service_stats = stats.get_service_model_stats()
        self.assertTrue(isinstance(service_stats, dict))
        self.assertEqual(service_stats["service_count"], 3)
        self.assertEqual(len(service_stats["service_name_aggregation"]), 5)
        self.assertEqual(
            service_stats["service_name_aggregation"][0]["name"],
            "Stockage numérique sécurisé",
        )
