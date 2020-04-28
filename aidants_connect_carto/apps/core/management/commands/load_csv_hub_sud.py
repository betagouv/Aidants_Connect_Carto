# flake8: noqa

import csv
import time

from django.core.management import BaseCommand

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import Place, Service, DataSource


def create_place(row, source_id):
    print("in place")
    place = Place()

    place.name = row["NOM DU LIEUX"]
    place.supporting_structure_name = row["STRUCTURE PORTEUSE"]
    place.type = "tiers lieu"  # row["TYPE DE LIEU"]
    place.legal_entity_type = utilities.process_legal_entity_type(
        row["NATURE JURIDIQUE"]
    )

    # address
    place.address_raw = utilities.clean_address_raw(
        row["ADRESSE"], row["CODE POSTAL"], row["VILLE"]
    )
    address_api_results_processed = utilities.process_address(place.address_raw)
    if address_api_results_processed:
        place.address_housenumber = address_api_results_processed["housenumber"]
        place.address_street = address_api_results_processed["street"]
        place.address_postcode = address_api_results_processed["postcode"]
        place.address_citycode = address_api_results_processed["citycode"]
        place.address_city = address_api_results_processed["city"]
        place.address_departement_code = address_api_results_processed[
            "departement_code"
        ]
        place.address_departement_name = address_api_results_processed[
            "departement_name"
        ]
        place.address_region_name = address_api_results_processed["region_name"]
        place.latitude = address_api_results_processed["latitude"]
        place.longitude = address_api_results_processed["longitude"]

    place.contact_website_url = row["PLUS D'INFORMATION"]
    place.contact_facebook_url = row["URL FACEBOOK"]
    place.contact_twitter_url = row["URL TWITTER"]
    place.contact_youtube_url = row["URL YOUTUBE"]

    place.opening_hours_raw = row["HORAIRES"]
    place.opening_hours_osm_format = utilities.process_opening_hours_to_osm_format(
        row["HORAIRES"]
    )

    place.additional_information = {
        "id": row["ID"],
        "type": row["TYPE DE LIEU"],
        "latitude": row["LATITUDE"],
        "longitude": row["LONGITUDE"],
        "activites_proposees": row["ACTIVITES PROPOSEES"],
        "materiels_disponibles": row["MATERIELS DISPONIBLES"],
        "autres_labels": row["AUTRES LABELS"],
    }

    place.logo_url = row["LOGO"]

    place.data_source_id = source_id

    place.save()
    print(row["ID"], "-->", place.id)
    # return place


class Command(BaseCommand):
    """
    python manage.py load_csv_hub_sud --path "data/hub_sud/Copie de Lieux Médiation_fablab_SudLab_LABELS.csv"
    """

    help = "Load a csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]

        source = DataSource.objects.create(name="Hub du Sud", type="hub")

        with open(path, "rt") as f:
            reader = csv.DictReader(f, delimiter=";")
            # print(reader.fieldnames)

            for index, row in enumerate(reader):
                if index < 150:  # all
                    time.sleep(1)
                    # print(index, row)

                    # place = create_place(row)
                    create_place(row, source.id)
