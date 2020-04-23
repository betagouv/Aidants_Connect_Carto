# flake8: noqa
from django.test import tag, TestCase

from aidants_connect_carto.apps.core import utilities


@tag("utilities")
class UtilitiesTestCase(TestCase):
    def test_process_opening_hours_to_osm_format(self):
        opening_hours_list = [
            (
                "Du lundi au vendredi : 09:00-12:00 et 14:00-16:30 / Samedi : 09:00-12:00",
                "Mo-Fr 09:00-12:00,14:00-16:30; Sa 09:00-12:00",
            ),
            (
                "Du lundi au vendredi de 8h30 à 12h et de 14h à 17h30",
                "Mo-Fr 08:30-12:00,14:00-17:30",
            ),
            (
                "du lundi au vendredi de 9h00 à 12h00 et de 13h30 à 16h30",
                "Mo-Fr 09:00-12:00,13:30-16:30",
            ),
            ("8h30-12h00/13h30-17h30", "08:30-12:00; 13:30-17:30"),
            (
                "Lundi : 13h30 - 17h30 ; Mardi au Jeudi : 8h30 - 12h et 13h30 - 17h30 ;  Vendredi : 8h30 - 12h et 13h30 - 16h",
                "Mo 13:30-17:30; Tu-Th 08:30-12:00,13:30-17:30; Fr 08:30-12:00,13:30-16:00",
            ),
            (
                "mardi de 10h à 21h / du mercredi au vendredi de 10h à 18h / le samedi de 9h15 à 18h",
                "Tu 10:00-21:00; We-Fr 10:00-18:00; Sa 09:15-18:00",
            ),
            (
                "Lundi au vendredi 8H00 à 17H30 et samedi 8H30 à 12H30",
                "Mo-Fr 08:00-17:30, Sa 08:30-12:30",
            ),
            ("Lundi", ""),  # fail
        ]
        for opening_hours in opening_hours_list:
            opening_hours_raw = opening_hours[0]
            opening_hours_osm_format = opening_hours[1]
            opening_hours_raw_processed = utilities.process_opening_hours_to_osm_format(
                opening_hours_raw
            )
            self.assertEqual(opening_hours_raw_processed, opening_hours_osm_format)

    def test_process_phone_number(self):
        phone_number_list = [
            ("01 23 45 67 89", "0123456789"),
            ("01.23.45.67.89", "0123456789"),
            ("01-23-45-67-89", "0123456789"),
            ("3960 (Service 0,06 € / mn + prix appel)", ""),
            (
                "0810 25 59 80* (0,06 €/mn + prix appel)  Un conseiller vous répond du lundi au vendredi de 9h à 16h00",
                "",
            ),
        ]
        for phone_number in phone_number_list:
            phone_number_raw = phone_number[0]
            phone_number_formatted = phone_number[1]
            phone_number_raw_processed = utilities.process_phone_number(
                phone_number_raw
            )
            self.assertEqual(phone_number_raw_processed, phone_number_formatted)

    def test_process_address(self):
        address_list = [
            (
                "20 Avenue de Ségur 75007 Paris",
                "20 Avenue de Ségur 75007 Paris",
                "Paris",
                "Île-de-France",
            )
        ]
        for address in address_list:
            address_raw = address[0]
            address_formatted = address[1]
            address_departement = address[2]
            address_region = address[3]
            address_raw_processed = utilities.process_address(address_raw)
            address_raw_processed_cleaned = f"{address_raw_processed['housenumber']} {address_raw_processed['street']} {address_raw_processed['postcode']} {address_raw_processed['city']}"
            self.assertEqual(address_raw_processed_cleaned, address_formatted)
            self.assertEqual(
                address_raw_processed["departement_name"], address_departement
            )
            self.assertEqual(address_raw_processed["region_name"], address_region)
