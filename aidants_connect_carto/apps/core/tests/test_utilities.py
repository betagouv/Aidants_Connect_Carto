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
