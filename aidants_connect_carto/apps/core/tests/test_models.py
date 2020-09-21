from django.test import TestCase

from aidants_connect_carto.apps.core.models import DataSource, DataSet, Place, Service


class DataSourceAndDataSetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_source_1 = DataSource.objects.create(name="Region Test", type="region")
        cls.data_set_1 = DataSet.objects.create(
            name="Lieux EPN 2019", data_source_id=cls.data_source_1.id
        )
        cls.data_set_2 = DataSet.objects.create(
            name="Tiers Lieux", data_source_id=cls.data_source_1.id
        )
        cls.place_1 = Place.objects.create(
            name="Lieu Test 1",
            address_region_name="Auvergne-Rhône-Alpes",
            data_set_id=cls.data_set_1.id,
        )
        cls.place_2 = Place.objects.create(
            name="Lieu Test 2", data_set_id=cls.data_set_2.id,
        )

    def test_retrieve_data_source_instance(self):
        self.assertEqual(str(self.data_source_1), "Region Test")
        self.assertEqual(self.data_source_1.data_set_count, 2)
        self.assertEqual(self.data_source_1.place_count, 2)

    def test_retrieve_data_set_instance(self):
        self.assertEqual(str(self.data_set_1), "Lieux EPN 2019")
        self.assertEqual(self.data_set_1.place_count, 1)


class PlaceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_source_1 = DataSource.objects.create(name="Region Test", type="region")
        cls.data_set_1 = DataSet.objects.create(
            name="Lieux EPN 2019", data_source_id=cls.data_source_1.id
        )
        cls.place_1 = Place.objects.create(
            name="Lieu Test 1",
            data_set_id=cls.data_set_1.id,
            address_housenumber="20",
            address_street="Avenue de Ségur",
            address_postcode="75007",
            address_city="Paris",
            address_region_name="Île-de-France",
        )
        Service.objects.create(
            name="Stockage numérique sécurisé", place_id=cls.place_1.id
        )
        cls.place_2 = Place.objects.create(
            name="Lieu Test 2",
            address_street="Place de la République",
            address_postcode="75021",
            address_city="Paris",
            address_region_name="Île-de-France",
            opening_hours_osm_format="Mo-Th 09:00-19:00, Fr 09:00-12:00",
        )

    def test_retrieve_place_instance(self):
        self.assertEqual(str(self.place_1), "Lieu Test 1")
        self.assertEqual(str(self.place_1.data_set), "Lieux EPN 2019")
        self.assertEqual(self.place_1.service_list, ["Stockage numérique sécurisé"])
        self.assertEqual(self.place_1.service_count, 1)

    def test_display_place_address_full(self):
        self.assertEqual(
            self.place_1.display_address_full, "20 Avenue de Ségur, 75007 Paris"
        )
        self.assertEqual(
            self.place_2.display_address_full, "Place de la République, 75021 Paris"
        )


class ServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.place_1 = Place.objects.create(
            name="Lieu Test 1", address_region_name="Auvergne-Rhône-Alpes",
        )
        cls.service_1 = Service.objects.create(
            name="Stockage numérique sécurisé", place_id=cls.place_1.id
        )

    def test_retrieve_service_instance(self):
        self.assertEqual(str(self.service_1), "Stockage numérique sécurisé")
        self.assertEqual(str(self.service_1.place), "Lieu Test 1")
