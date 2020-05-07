# flake8: noqa

import csv
import time

from django.core.management import BaseCommand

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import Place, Service, DataSource


"""
import_config: JSONField
- dataset_file_delimiter
- place_fields_set
- place_fields_mapping_auto
- place_fields_mapping_boolean
- place_fields_mapping_process
- place_fields_mapping_additional_information
"""


def create_place(row, data_source):
    print("in place")

    place_dict = {}

    for elem in data_source.import_config.get("place_fields_set", []):
        place_dict[elem["place_field"]] = elem["value"]

    for elem in data_source.import_config.get("place_fields_mapping_auto", []):
        place_dict[elem["place_field"]] = row[elem["file_field"]]

    for elem in data_source.import_config.get("place_fields_mapping_boolean", []):
        place_dict[elem["place_field"]] = utilities.process_boolean(
            row[elem["file_field"]]
        )

    for elem in data_source.import_config.get("place_fields_mapping_process", []):
        if elem["place_field"] == "legal_entity_type":
            place_dict["legal_entity_type"] = utilities.process_legal_entity_type(
                row[elem["file_field"]]
            )

        if elem["place_field"] == "address_raw":
            """
            Different options:
            - "20 Avenue de Ségur 75007 Paris"
            - ["20 Avenue de Ségur", "75007", "Paris"]
            - [["20", "Avenue", "de Ségur"], "75007", "Paris"]
            """
            if type(elem["file_field"]) == list:
                address_temp = ""
                if type(elem["file_field"][0]) == list:
                    address_temp = " ".join(
                        [
                            row[item].strip()
                            for item in elem["file_field"][0]
                            if item not in ["", "0", 0, False, None]
                        ]
                    )
                else:
                    address_temp = row[elem["file_field"][0]]
                place_dict["address_raw"] = utilities.clean_address_raw_list(
                    address=address_temp,
                    postcode=row[elem["file_field"][1]],
                    city=row[elem["file_field"][2]],
                )
            else:
                place_dict["address_raw"] = row[elem["file_field"]]
            address_api_results_processed = utilities.process_address(
                place_dict["address_raw"]
            )
            if address_api_results_processed:
                place_dict["address_housenumber"] = address_api_results_processed[
                    "housenumber"
                ]
                place_dict["address_street"] = address_api_results_processed["street"]
                place_dict["address_postcode"] = address_api_results_processed[
                    "postcode"
                ]
                place_dict["address_citycode"] = address_api_results_processed[
                    "citycode"
                ]
                place_dict["address_city"] = address_api_results_processed["city"]
                place_dict["address_departement_code"] = address_api_results_processed[
                    "departement_code"
                ]
                place_dict["address_departement_name"] = address_api_results_processed[
                    "departement_name"
                ]
                place_dict["address_region_name"] = address_api_results_processed[
                    "region_name"
                ]
                place_dict["latitude"] = address_api_results_processed["latitude"]
                place_dict["longitude"] = address_api_results_processed["longitude"]

        if elem["place_field"] == "contact_phone_raw":
            place_dict["contact_phone_raw"] = row[elem["file_field"]]
            place_dict["contact_phone"] = utilities.process_phone_number(
                place_dict["contact_phone_raw"]
            )

        if elem["place_field"] == "opening_hours_raw":
            """
            Different options:
            - "du lundi au vendredi de 9h à 18h"
            - ["Lundi: 9h-18h", "Mardi: 9h-12h"]
            """
            if type(elem["file_field"]) == list:
                place_dict["opening_hours_raw"] = "|".join(
                    [row[item] for item in elem["file_field"]]
                )
            else:
                place_dict["opening_hours_raw"] = row[elem["file_field"]]
            place_dict[
                "opening_hours_osm_format"
            ] = utilities.process_opening_hours_to_osm_format(
                place_dict["opening_hours_raw"]
            )

    place_dict["additional_information"] = {}
    for elem in data_source.import_config.get(
        "place_fields_mapping_additional_information", []
    ):
        place_dict["additional_information"][elem["place_field"]] = row[
            elem["file_field"]
        ]

    place_dict["data_source_id"] = data_source.id

    place = Place.objects.create(**place_dict)
    # print(row["ID"], "-->", place.id)
    print("-->", place.id)
    # return place


class Command(BaseCommand):
    """
    python manage.py load_data_source_csv --id 11
    """

    help = "Load a csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--id", type=int)

    def handle(self, *args, **kwargs):
        data_source_id = kwargs["id"]

        data_source = DataSource.objects.get(pk=data_source_id)

        # encoding="utf-8-sig" for files that start with '\ufeff'
        with open(data_source.dataset_local_path, mode="rt", encoding="utf-8-sig") as f:
            FILE_DELIMITER = data_source.import_config.get(
                "dataset_file_delimiter", ";"
            )
            reader = csv.DictReader(f, delimiter=FILE_DELIMITER)
            # print(reader.fieldnames)
            print(data_source.name)

            for index, row in enumerate(reader):
                time.sleep(1)
                print(index, row)

                # place = create_place(row)
                create_place(row, data_source)