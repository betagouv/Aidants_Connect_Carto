# flake8: noqa
from datetime import date, datetime

from freezegun import freeze_time

from django.test import TestCase

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities


class UtilitiesOpeningHoursTest(TestCase):
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
            ("8h30-12h00/13h30-17h30", "08:30-12:00,13:30-17:30"),
            (
                "Lundi : 13h30 - 17h30 ; Mardi au Jeudi : 8h30 - 12h et 13h30 - 17h30 ;  Vendredi : 8h30 - 12h et 13h30 - 16h",
                # "Mo 13:30-17:30; Tu-Th 08:30-12:00,13:30-17:30; Fr 08:30-12:00,13:30-16:00",
                "",  # not managed anymore because of ";" (considers that there is 1 day per elem split)
            ),
            (
                "mardi de 10h à 21h / du mercredi au vendredi de 10h à 18h / le samedi de 9h15 à 18h",
                "Tu 10:00-21:00; We-Fr 10:00-18:00; Sa 09:15-18:00",
            ),
            (
                "Lundi au vendredi 8H00 à 17H30 et samedi 8H30 à 12H30",
                "Mo-Fr 08:00-17:30, Sa 08:30-12:30",
            ),
            (
                "Mercredi 14h-18h; jeudi 18h-21h; vendredi 9h-12h/14h-18h; samedi 14h-18h",
                # "We 14:00-18:00; Th 18:00-21:00; Fr 09:00-12:00,14:00-18:00; Sa 14:00-18:00",
                "",  # not managed anymore because of ";" (considers that there is 1 day per elem split)
            ),
            (
                "Lundi 9h-12h/14h-21h; mardi 9h-12h/14h-18h;mercredi 9h-12h/14h-21h; jeudi et vendredi 9h-12h/14h-18h; samedi 9h-12h",
                # "Mo 09:00-12:00,14:00-21:00; Tu 09:00-12:00,14:00-18:00; We 09:00-12:00,14:00-21:00; Th, Fr 09:00-12:00,14:00-18:00; Sa 09:00-12:00",
                "",  # not managed anymore because of ";" (considers that there is 1 day per elem split)
            ),
            ("Du lundi au samedi de 9-13h/14h-20h", "Mo-Sa 09:00-13:00,14:00-20:00"),
            # Array --> string with " | " seperator
            (
                "9:00 - 12:00 / 13:30 - 17:00 | 9:00 - 12:00 / 13:30 - 17:00 |  |  | - | 10:00 - 13:00 | -",
                "Mo 09:00-12:00,13:30-17:00; Tu 09:00-12:00,13:30-17:00; Sa 10:00-13:00",
            ),
            (
                "9:00 - 12:00 / 13:30 - 17:00 | 9:00 - 12:00",
                "Mo 09:00-12:00,13:30-17:00; Tu 09:00-12:00",
            ),
            # Array --> string with "; " seperator
            (
                "9:00 - 12:00 / 13:30 - 17:00; 9:00 - 12:00 / 13:30 - 17:00; ; ; -; 10:00 - 13:00; -",
                "Mo 09:00-12:00,13:30-17:00; Tu 09:00-12:00,13:30-17:00; Sa 10:00-13:00",
            ),
            (
                "9:00 - 12:00 / 13:30 - 17:00; 9:00 - 12:00",
                "Mo 09:00-12:00,13:30-17:00; Tu 09:00-12:00",
            ),
            # (
            #     "9:00 - 12:00 / 13:30 - 17:00",
            #     "09:00-12:00,13:30-17:00"
            # ),
            # fail
            (
                "du lundi au vendredi de 9 à 12 h et de 14 à 18 h, le samedi de 10 à 13 h",
                "",
            ),
            (
                "Lundi : 9:00 - 12:00 / 13:30 - 17:00; Mardi : 9:00 - 12:00 / 13:30 - 17:00; Samedi : -",
                "",
            ),
            ("Mo 10:00-13:00,après-midi sur rdv", ""),
            ("Lundi", ""),
            (
                [
                    "9h - 18h",
                    "9h à 12h - 13h30 à 17h",
                    "14h00 à 18h30",
                    "9/17",
                    "9h - 18h",
                    "fermé",
                    "",
                ],
                "",  # "Mo 9h-18h; Tu 9h-12h,13:30-17h; We 14:00-18:30; Th 9,17; Fr 9h-18h; Sa off",
            ),
        ]
        for opening_hours in opening_hours_list:
            opening_hours_raw = opening_hours[0]
            opening_hours_osm_format = opening_hours[1]
            opening_hours_raw_processed = utilities.process_opening_hours_to_osm_format(
                opening_hours_raw
            )
            self.assertIsInstance(opening_hours_raw_processed, str)
            self.assertEqual(opening_hours_raw_processed, opening_hours_osm_format)

    def test_get_opening_hours_osm_format_description(self):
        opening_hours_osm_format_list = [
            ("Mo-Fr 09:00-19:00", ["Du lundi au vendredi : 09:00 – 19:00."]),
            (
                "Mo-Th 09:00-19:00; Fr 08:00-12:00",
                ["Du lundi au jeudi : 09:00 – 19:00.", "Le vendredi : 08:00 – 12:00."],
            ),
            ("", []),
        ]
        for opening_hours_osm_format in opening_hours_osm_format_list:
            opening_hours_osm_format_description = utilities.get_opening_hours_osm_format_description(
                opening_hours_osm_format[0]
            )
            self.assertIsInstance(opening_hours_osm_format_description, list)
            self.assertEqual(
                opening_hours_osm_format_description, opening_hours_osm_format[1]
            )

    def test_get_opening_hours_osm_format_week_description(self):
        opening_hours_osm_format_list = [
            (
                "Mo-Fr 09:00-19:00",
                [
                    "Lundi : 09:00 – 19:00",
                    "Mardi : 09:00 – 19:00",
                    "Mercredi : 09:00 – 19:00",
                    "Jeudi : 09:00 – 19:00",
                    "Vendredi : 09:00 – 19:00",
                    "Samedi : fermé",
                    "Dimanche : fermé",
                ],
            ),
            (
                "Mo-Th 09:00-19:00; Fr 08:00-12:00",
                [
                    "Lundi : 09:00 – 19:00",
                    "Mardi : 09:00 – 19:00",
                    "Mercredi : 09:00 – 19:00",
                    "Jeudi : 09:00 – 19:00",
                    "Vendredi : 08:00 – 12:00",
                    "Samedi : fermé",
                    "Dimanche : fermé",
                ],
            ),
            ("", []),
        ]
        for opening_hours_osm_format in opening_hours_osm_format_list:
            opening_hours_osm_format_week_description = utilities.get_opening_hours_osm_format_week_description(
                opening_hours_osm_format[0]
            )
            self.assertIsInstance(opening_hours_osm_format_week_description, list)
            self.assertEqual(
                opening_hours_osm_format_week_description, opening_hours_osm_format[1]
            )

    @freeze_time("2020-05-15 15:00:00")  # Friday 3PM
    def test_get_opening_hours_osm_format_today(self):
        opening_hours_osm_format_list = [
            ("Mo-Fr 09:00-19:00", [1, "2020-05-15 09:00:00", "2020-05-15 19:00:00"]),
            (
                "Mo-Th 09:00-19:00; Fr 08:00-12:00",
                [1, "2020-05-15 08:00:00", "2020-05-15 12:00:00"],
            ),
            (
                "Fr 08:00-12:00,14:00-18:00",
                [
                    2,
                    "2020-05-15 08:00:00",
                    "2020-05-15 12:00:00",
                    "2020-05-15 14:00:00",
                    "2020-05-15 18:00:00",
                ],
            ),
            ("", []),
        ]
        for opening_hours_osm_format in opening_hours_osm_format_list:
            opening_hours_osm_format_today = utilities.get_opening_hours_osm_format_today(
                opening_hours_osm_format[0]
            )
            self.assertIsInstance(opening_hours_osm_format_today, list)
            if len(opening_hours_osm_format_today) > 0:
                opening_hours_osm_format_today_length = opening_hours_osm_format[1][0]
                opening_hours_osm_format_today_beginning_datetime = opening_hours_osm_format[
                    1
                ][
                    1
                ]
                opening_hours_osm_format_today_end_datetime = opening_hours_osm_format[
                    1
                ][2]
                self.assertEqual(
                    len(opening_hours_osm_format_today),
                    opening_hours_osm_format_today_length,
                )
                self.assertEqual(
                    str(opening_hours_osm_format_today[0].beginning),
                    opening_hours_osm_format_today_beginning_datetime,
                )
                self.assertEqual(
                    str(opening_hours_osm_format_today[0].end),
                    opening_hours_osm_format_today_end_datetime,
                )
                if len(opening_hours_osm_format_today) > 1:
                    opening_hours_osm_format_today_afternoon_beginning_datetime = opening_hours_osm_format[
                        1
                    ][
                        3
                    ]
                    opening_hours_osm_format_today_afternoon_end_datetime = opening_hours_osm_format[
                        1
                    ][
                        4
                    ]
                    self.assertEqual(
                        str(opening_hours_osm_format_today[1].beginning),
                        opening_hours_osm_format_today_afternoon_beginning_datetime,
                    )
                    self.assertEqual(
                        str(opening_hours_osm_format_today[1].end),
                        opening_hours_osm_format_today_afternoon_end_datetime,
                    )

    @freeze_time("2020-05-15 15:00:00")  # Friday 3PM
    def test_get_opening_hours_osm_format_today(self):
        opening_hours_osm_format_list = [
            ("Mo-Fr 09:00-19:00", True),
            ("Mo-Th 09:00-19:00; Fr 08:00-12:00", False),
            ("Fr 08:00-12:00,14:00-18:00", True),
            ("Mo-Th 09:00-19:00", False),
            ("", False),
        ]
        for opening_hours_osm_format in opening_hours_osm_format_list:
            opening_hours_osm_format_today = utilities.get_opening_hours_osm_format_is_open(
                opening_hours_osm_format[0]
            )
            self.assertIsInstance(opening_hours_osm_format_today, bool)
            self.assertEqual(
                opening_hours_osm_format_today, opening_hours_osm_format[1]
            )


class UtilitiesPhoneTest(TestCase):
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


class UtilitiesAddressTest(TestCase):
    def test_clean_address_raw_list(self):
        address_raw_list = [
            ("11 place d’armes", "83000", "TOULON", "11 place d’armes 83000 TOULON"),
            (
                "24 avenue des Diables Bleus",
                "6300",
                "NICE",
                "24 avenue des Diables Bleus 06300 NICE",
            ),
            (
                "Place de Verdun",
                "4170",
                "SAINT-ANDRE-LES-ALPES",
                "Place de Verdun 04170 SAINT-ANDRE-LES-ALPES",
            ),
        ]
        for address_raw in address_raw_list:
            address_raw_cleaned = utilities.clean_address_raw_list(
                address_raw[0], address_raw[1], address_raw[2]
            )
            self.assertEqual(address_raw_cleaned, address_raw[3])

    def test_process_address(self):
        address_list = [
            (
                "20 Avenue de Ségur 75007 Paris",
                ["20 Avenue de Ségur 75007 Paris", "Paris", "Île-de-France"],
            ),
            (
                "Rue case toto 97217 Les Anses-d'Arlet",
                ["Rue Case Toto 97217 Les Anses-d'Arlet", "Martinique", "Martinique"],
            ),
            # unknown address
            ("Couveuse Potentiel 58022 NEVERS", [None, None, None]),
        ]
        for address in address_list:
            address_raw = address[0]
            address_formatted = address[1][0]
            address_departement = address[1][1]
            address_region = address[1][2]
            address_raw_processed = utilities.process_address(address_raw)
            if address_raw_processed:
                address_raw_processed_cleaned = f"{address_raw_processed['housenumber']}{' ' if address_raw_processed['housenumber'] else ''}{address_raw_processed['street']} {address_raw_processed['postcode']} {address_raw_processed['city']}"
                self.assertEqual(address_raw_processed_cleaned, address_formatted)
                self.assertEqual(
                    address_raw_processed["departement_name"], address_departement
                )
                self.assertEqual(address_raw_processed["region_name"], address_region)
            else:
                self.assertEqual(address_raw_processed, address_raw_processed)

    def test_get_address_full(self):
        address_list = [
            (
                ["20", "Avenue de Ségur", "75007", "Paris"],
                "20 Avenue de Ségur, 75007 Paris",
            ),
            (
                ["", "Place de la République", "75021", "Paris"],
                "Place de la République, 75021 Paris",
            ),
            (["", "", "38000", "Grenoble"], "38000 Grenoble"),
            (["", "", "", ""], ""),
            ([None, "", "", ""], ""),
        ]
        for address in address_list:
            address_full = utilities.get_address_full(
                address[0][0], address[0][1], address[0][2], address[0][3]
            )
            self.assertEqual(address_full, address[1])


class UtilitiesIsOnline(TestCase):
    is_online_list = [
        # (input, db_output, file_output)
        ("Oui", True, "Oui"),
        ("En effet", True, "Oui"),
        ("", False, "Non"),
    ]

    def test_is_online(self):
        for is_online in self.is_online_list:
            self.assertEqual(utilities.process_is_online(is_online[0]), is_online[1])

    def test_is_online_to_file(self):
        for is_online in self.is_online_list:
            self.assertEqual(
                utilities.process_is_online(is_online[0], destination="file"),
                is_online[2],
            )


class UtilitiesTypeTest(TestCase):
    place_type_list = [
        # (input, db_output, file_output)
        (
            "CAF",
            "securite sociale",
            "Organisme de sécurité sociale (CAF, CPAM, CARSAT, MSA...)",
        ),
        ("", constants.CHOICE_OTHER, constants.EMPTY_STRING),
    ]

    def test_process_type(self):
        for place_type in self.place_type_list:
            self.assertEqual(utilities.process_type(place_type[0]), place_type[1])

    def test_process_type_to_file(self):
        for place_type in self.place_type_list:
            self.assertEqual(
                utilities.process_type(place_type[0], destination="file"), place_type[2]
            )


class UtilitiesStatusTest(TestCase):
    status_list = [
        # (input, db_output, file_output)
        ("Public", "public", "Public"),
        ("Privé", "prive", "Privé"),
        ("", constants.CHOICE_OTHER, constants.EMPTY_STRING),
    ]

    def test_process_status(self):
        for status in self.status_list:
            self.assertEqual(utilities.process_status(status[0]), status[1])

    def test_process_status_to_file(self):
        for status in self.status_list:
            self.assertEqual(
                utilities.process_status(status[0], destination="file"), status[2]
            )


class UtilitiesLegalEntityTypeTest(TestCase):
    legal_entity_type_list = [
        # (input, db_output, file_output)
        ("association", "association", "Association"),
        ("CAE", "cae", "Coopérative d'Activités et d'Entrepreneur·es (CAE)"),
        ("", constants.CHOICE_OTHER, constants.EMPTY_STRING),
    ]

    def test_process_legal_entity_type(self):
        for legal_entity_type in self.legal_entity_type_list:
            self.assertEqual(
                utilities.process_legal_entity_type(legal_entity_type[0]),
                legal_entity_type[1],
            )

    def test_process_legal_entity_type_to_file(self):
        for legal_entity_type in self.legal_entity_type_list:
            self.assertEqual(
                utilities.process_legal_entity_type(
                    legal_entity_type[0], destination="file"
                ),
                legal_entity_type[2],
            )


class UtilitiesTargetAudienceTest(TestCase):
    target_audience_list = [
        # (input, db_output, file_output)
        ("Droits des étrangers", ["etranger"], "Étrangers"),
        ("Personnes de nationalité étrangère", ["etranger"], "Étrangers"),
        ("Moins de 26 ans", ["jeune"], "Jeunes"),
        ("PLUS DE 50 ANS", ["senior"], "Séniors"),
        (
            "Personnes en situation de handicap, Personnes en recherche d'emploi",
            ["demandeur emploi", "handicap"],
            "Demandeurs d'emploi,Personnes en situation de handicap",
        ),
        ("Inconnu", [], ""),
        ("", [], ""),
    ]

    def test_process_target_audience(self):
        for target_audience in self.target_audience_list:
            self.assertEqual(
                utilities.process_target_audience(target_audience[0]),
                target_audience[1],
            )

    def test_process_target_audience_to_file(self):
        for target_audience in self.target_audience_list:
            self.assertEqual(
                utilities.process_target_audience(
                    target_audience[0], destination="file"
                ),
                target_audience[2],
            )


class UtilitiesSupportAccessTest(TestCase):
    support_access_list = [
        # (input, db_output, file_output)
        ("sur Rendez-Vous", ["inscription"], "Sur inscription ou rendez-vous"),
        ("sans Rendez-Vous", ["libre"], "Accès libre"),
        (
            "libre, réservation",
            ["libre", "inscription"],
            "Accès libre,Sur inscription ou rendez-vous",
        ),
        ("RDV", ["inscription"], "Sur inscription ou rendez-vous"),
        ("'accès en mairie aux heures d'ouverture et sur rendez vous'", [], ""),
        ("Accès libre - accompagnement si besoin", [], ""),
        ("Inconnu", [], ""),
        ("", [], ""),
    ]

    def test_process_support_access(self):
        for support_access in self.support_access_list:
            self.assertEqual(
                utilities.process_support_access(support_access[0]), support_access[1],
            )

    def test_process_support_access_to_file(self):
        for support_access in self.support_access_list:
            self.assertEqual(
                utilities.process_support_access(support_access[0], destination="file"),
                support_access[2],
            )


class UtilitiesSupportModeTest(TestCase):
    support_mode_list = [
        # (input, db_output, file_output)
        ("individuel", ["individuel"], "Individuel"),
        ("accompagnement personnalisé", ["individuel"], "Individuel"),
        ("Individuel, collectif", ["individuel", "collectif"], "Individuel,Collectif"),
        ("Inconnu", [], ""),
        ("", [], ""),
    ]

    def test_process_support_mode(self):
        for support_mode in self.support_mode_list:
            self.assertEqual(
                utilities.process_support_mode(support_mode[0]), support_mode[1],
            )

    def test_process_support_mode_to_file(self):
        for support_mode in self.support_mode_list:
            self.assertEqual(
                utilities.process_support_mode(support_mode[0], destination="file"),
                support_mode[2],
            )


class UtilitiesLabelsTest(TestCase):
    labels_list = [
        # (input, db_output, file_output)
        ("aptic", ["APTIC"], "APTIC"),
        ("aptic, mfs", ["APTIC", "France Services"], "APTIC,France Services"),
        ("Aidants connect", ["Aidants Connect"], "Aidants Connect"),
        ("MFS,France Service", ["France Services"], "France Services"),
        ("tiers-lieux", [], ""),
        ("Inconnu", [], ""),
        ("", [], ""),
    ]

    def test_process_labels(self):
        for labels in self.labels_list:
            self.assertEqual(
                utilities.process_labels(labels[0]), labels[1],
            )

    def test_process_labels_to_file(self):
        for labels in self.labels_list:
            self.assertEqual(
                utilities.process_labels(labels[0], destination="file"), labels[2],
            )


class UtilitiesServiceSimpleTest(TestCase):
    process_service_name_list = [
        # (input, db_output)
        # file_output ? same as db_output
        ("Etre initié aux outils numériques", "Acquisition de compétences numériques"),
        ("", constants.EMPTY_STRING),
    ]

    def test_process_service_name(self):
        for process_service_name in self.process_service_name_list:
            self.assertEqual(
                utilities.process_service_name(process_service_name[0]),
                process_service_name[1],
            )

    def test_process_service_name_to_file(self):
        for process_service_name in self.process_service_name_list:
            self.assertEqual(
                utilities.process_service_name(
                    process_service_name[0], destination="file"
                ),
                process_service_name[1],
            )


class UtilitiesServiceTest(TestCase):
    process_service_name_list = [
        # (input, db_output, file_output)
        (
            "Etre initié aux outils numériques",
            ["Acquisition de compétences numériques"],
            "Acquisition de compétences numériques",
        ),
        (
            "Accès à Internet en autonomie, Etre accompagné dans ses démarches administratives",
            [
                "Accompagnement aux démarches administratives en ligne",
                "Accès à un équipement informatique",
            ],
            "Accompagnement aux démarches administratives en ligne,Accès à un équipement informatique",
        ),
        ("", [], constants.EMPTY_STRING),
    ]

    def test_process_service_name(self):
        for process_service_name in self.process_service_name_list:
            self.assertEqual(
                utilities.process_services(process_service_name[0]),
                process_service_name[1],
            )

    def test_process_service_name_to_file(self):
        for process_service_name in self.process_service_name_list:
            self.assertEqual(
                utilities.process_services(process_service_name[0], destination="file"),
                process_service_name[2],
            )
