# flake8: noqa

import csv
import json
import time

from django.core.management import BaseCommand

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import DataSource, DataSet, Place, Service


def get_or_create_data_source(data_set_import_config_file):
    print("in data_source")

    with open(data_set_import_config_file) as json_file:
        data_set_import_config = json.load(json_file)

        data_source_dict = {}

        data_source_dict["name"] = data_set_import_config["data_source_name"]
        data_source_dict["type"] = data_set_import_config["data_source_type"]

        data_source, created = DataSource.objects.get_or_create(**data_source_dict)
        print("-->", data_source.id, "created ?", created)
        return data_source


def create_data_set(data_source, data_set_import_config_file):
    print("in data_set")

    with open(data_set_import_config_file) as json_file:
        data_set_import_config = json.load(json_file)

        data_set_dict = {}

        data_set_dict["name"] = data_set_import_config["name"]
        data_set_dict["url"] = data_set_import_config["url"]
        data_set_dict["local_path"] = data_set_import_config["file_path"]
        data_set_dict["last_updated"] = data_set_import_config["last_updated"]
        data_set_dict["import_config"] = data_set_import_config["import_config"]
        data_set_dict["import_comment"] = data_set_import_config["import_comment"]

        data_set_dict["data_source_id"] = data_source.id

        data_set = DataSet.objects.create(**data_set_dict)
        print("-->", data_set.id)
        return data_set


"""
import_config: JSONField
- dataset_file_delimiter
- place_fields_set
- place_fields_mapping_auto
- place_fields_mapping_boolean
- place_fields_mapping_process
- place_fields_mapping_additional_information
"""


def create_place(row, data_set):
    print("in place")

    place_dict = {}

    """
    place_fields_set
    """
    for elem in data_set.import_config.get("place_fields_set", []):
        if "type" in elem:
            if elem["type"] == "boolean":
                place_dict[elem["place_field"]] = bool(elem["value"] == "true")
        else:
            place_dict[elem["place_field"]] = elem["value"]

    """
    place_fields_mapping_auto
    """
    for elem in data_set.import_config.get("place_fields_mapping_auto", []):
        place_dict[elem["place_field"]] = row[elem["file_field"]]

    """
    place_fields_mapping_boolean
    """
    for elem in data_set.import_config.get("place_fields_mapping_boolean", []):
        place_dict[elem["place_field"]] = utilities.process_boolean(
            row[elem["file_field"]]
        )

    """
    place_fields_mapping_process
    - type
    - status
    - legal_entity_type
    - target_audience_raw
    - support_access_raw
    - support_mode_raw
    - address_raw
    - contact_phone_raw
    - opening_hours_raw
    """
    for elem in data_set.import_config.get("place_fields_mapping_process", []):
        if elem["place_field"] == "type":
            place_dict["type"] = utilities.process_type(row[elem["file_field"]])

        if elem["place_field"] == "status":
            place_dict["status"] = utilities.process_status(row[elem["file_field"]])

        if elem["place_field"] == "legal_entity_type":
            place_dict["legal_entity_type"] = utilities.process_legal_entity_type(
                row[elem["file_field"]]
            )

        if elem["place_field"] == "target_audience_raw":
            place_dict["target_audience_raw"] = row[elem["file_field"]]
            place_dict["target_audience"] = utilities.process_target_audience(
                place_dict["target_audience_raw"]
            )

        if elem["place_field"] == "support_access_raw":
            place_dict["support_access_raw"] = row[elem["file_field"]]
            place_dict["support_access"] = utilities.process_support_access(
                place_dict["support_access_raw"]
            )

        if elem["place_field"] == "support_mode_raw":
            place_dict["support_mode_raw"] = row[elem["file_field"]]
            place_dict["support_mode"] = utilities.process_support_mode(
                place_dict["support_mode_raw"]
            )

        if elem["place_field"] == "address_raw":
            """
            Different options:
            - "20 Avenue de Ségur 75007 Paris"
            - ["20 Avenue de Ségur", "75007", "Paris"]
            - [["20", "Avenue", "de Ségur"], "75007", "Paris"]
            - ""
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
            - ""
            """
            if type(elem["file_field"]) == list:
                place_dict["opening_hours_raw"] = [
                    row[item] for item in elem["file_field"]
                ]
            else:
                place_dict["opening_hours_raw"] = row[elem["file_field"]]
            place_dict[
                "opening_hours_osm_format"
            ] = utilities.process_opening_hours_to_osm_format(
                place_dict["opening_hours_raw"]
            )

    """
    additional_information
    """
    place_dict["additional_information"] = {}
    for elem in data_set.import_config.get(
        "place_fields_mapping_additional_information", []
    ):
        place_dict["additional_information"][elem["place_field"]] = row[
            elem["file_field"]
        ]

    place_dict["data_set_id"] = data_set.id

    print(place_dict)
    place = Place.objects.create(**place_dict)
    # print(row["ID"], "-->", place.id)
    print("-->", place.id)
    return place


def create_service(row, data_set, place):
    print("in service")

    # service_dict = {}

    # get list of services
    service_name_list = row[
        data_set.import_config.get("place_service").get("file_field")
    ]
    if data_set.import_config.get("place_service").get("split_delimeter"):
        service_name_list = service_name_list.split(
            data_set.import_config.get("place_service").get("split_delimeter")
        )

    # create services
    for service_name in service_name_list:
        service_name_processed = utilities.process_service_name(service_name)
        if service_name_processed:
            service = Service.objects.create(
                place_id=place.id, name=service_name_processed
            )
            print("-->", service.id)
        else:
            print("=== process_service_name() failed", service_name)


class Command(BaseCommand):
    """
    python manage.py load_data_set_csv --id 11
    python manage.py load_data_set_csv --file data/hub_abc/hub_abc_import_config.json
    """

    help = "Load a data set (csv file) into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--id",
            help="L'id du fournisseur de donnée (dans la base de donnée)",
            type=int,
        )
        parser.add_argument(
            "--file", help="Le chemin vers la config du jeu de donnée", type=str
        )

    def handle(self, *args, **kwargs):
        data_source_id = kwargs["id"]
        data_set_file = kwargs["file"]

        # get or create data_source
        if data_source_id:
            data_source = DataSource.objects.get(pk=data_source_id)
        else:
            if data_set_file:
                data_source = get_or_create_data_source(data_set_file)
            else:
                print("--id or --file argument missing")

        if data_source:
            # create data_set
            data_set = create_data_set(data_source, data_set_file)

            if data_set:
                # encoding="utf-8-sig" for files that start with '\ufeff'
                with open(data_set.local_path, mode="rt", encoding="utf-8-sig") as f:
                    FILE_DELIMITER = data_set.import_config.get(
                        "dataset_file_delimiter", ";"
                    )
                    reader = csv.DictReader(f, delimiter=FILE_DELIMITER)
                    # print(reader.fieldnames)
                    print(data_set.name)

                    for index, row in enumerate(reader):
                        time.sleep(1)
                        print(index, row)

                        # place = create_place(row)
                        place = create_place(row, data_set)

                        if data_set.import_config.get("place_service", None):
                            create_service(row, data_set, place)
