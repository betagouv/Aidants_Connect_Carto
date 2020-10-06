# flake8: noqa

import csv
import json
import time

from django.core.management import BaseCommand

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import DataSource, DataSet, Place, Service


"""
import_config: JSONField
- dataset_file_delimiter
- place_fields_set
- place_fields_mapping_auto
- place_fields_mapping_boolean
- place_fields_mapping_process
- place_fields_mapping_additional_information
"""


def create_place_dict(row, data_set_import_config):
    print("in place")

    place_dict = {}

    """
    mapping_from_file
    --> output = file_field + '_mapped'
    """
    for elem in data_set_import_config.get("mapping_from_file", []):
        with open(elem["mapping_file_path"]) as data_file:
            json_data = json.load(data_file)
            if "seperator" in elem:
                # custom to Francil'IN
                elem_list = row[elem["file_field"]].split(elem["seperator"])
                elem_list_mapped = []
                for item in elem_list:
                    elem_list_mapped.append(json_data["themes"][item.strip()]["label"])
        place_dict[elem["file_field"] + "_mapped"] = ",".join(elem_list_mapped)

    """
    place_fields_set
    """
    for elem in data_set_import_config.get("place_fields_set", []):
        if "type" in elem:
            if elem["type"] == "boolean":
                place_dict[elem["place_field"]] = bool(elem["value"] == "true")
        else:
            place_dict[elem["place_field"]] = elem["value"]

    """
    place_fields_mapping_auto
    """
    for elem in data_set_import_config.get("place_fields_mapping_auto", []):
        place_dict[elem["place_field"]] = row[elem["file_field"]]

    """
    place_fields_mapping_boolean
    """
    for elem in data_set_import_config.get("place_fields_mapping_boolean", []):
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
    - contact_phone_raw
    - price_details
    - address_raw
    - opening_hours_raw
    """
    for elem in data_set_import_config.get("place_fields_mapping_process", []):
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

        if elem["place_field"] == "contact_phone_raw":
            place_dict["contact_phone_raw"] = row[elem["file_field"]]
            place_dict["contact_phone"] = utilities.process_phone_number(
                place_dict["contact_phone_raw"]
            )

        if elem["place_field"] == "price_details":
            place_dict["price_details"] = row[elem["file_field"]]
            place_dict["is_free"] = utilities.process_price(place_dict["price_details"])

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
    # place_dict["additional_information"] = {}
    # for elem in data_set_import_config.get(
    #     "place_fields_mapping_additional_information", []
    # ):
    #     if type(elem) == dict:
    #         place_dict["additional_information"][elem["place_field"]] = row[
    #             elem["file_field"]
    #         ]
    #     if type(elem) == str:
    #         place_dict["additional_information"][elem] = row[elem]

    # place_dict["data_set_id"] = data_set.id

    # print(place_dict)
    # place = Place.objects.create(**place_dict)
    # # print(row["ID"], "-->", place.id)
    # print("-->", place.id)
    # return place
    return place_dict


class Command(BaseCommand):
    """
    python manage.py enrich_data_set_csv --file data/hub_abc/hub_abc_import_config.json
    """

    help = "Enrich a dataset with data model columns"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            help="Le chemin vers la config du jeu de donnée",
            type=str,
            default=None,
        )

    def handle(self, *args, **kwargs):
        data_set_config_file = kwargs["file"]

        if not data_set_config_file:
            print("--file argument missing")
            return
        else:

            with open(data_set_config_file) as json_file:
                data_set_config = json.load(json_file)

                print("Data Set name:", data_set_config["name"])
                FILE_DELIMITER = data_set_config["import_config"].get(
                    "dataset_file_delimiter", ";"
                )

                # encoding="utf-8-sig" for files that start with '\ufeff'
                with open(
                    data_set_config["file_path"], mode="rt", encoding="utf-8-sig"
                ) as input_file:
                    print("data_set_config", data_set_config)

                    csvreader = csv.DictReader(input_file, delimiter=FILE_DELIMITER)

                    # add fieldnames (if they don't already exist)
                    # print(csvreader.fieldnames)
                    PLACE_FIELDS_TO_IGNORE = [
                        "id",
                        "has_equipment_wifi",
                        "has_equipment_computer",
                        "has_equipment_scanner",
                        "has_equipment_printer",
                        "equipment_other",
                        "has_accessibility_hi",
                        "has_accessibility_mi",
                        "has_accessibility_pi",
                        "has_accessibility_vi",
                        "languages",
                        "has_label_fs",
                        "logo_url",
                        "additional_information",
                        "data_set",
                        "osm_node_id",
                        "created_at",
                        "updated_at",
                    ]
                    fieldnames = (
                        [
                            f.name
                            for f in Place._meta.fields
                            if f.name not in PLACE_FIELDS_TO_IGNORE
                        ]
                        + [
                            elem["file_field"] + "_mapped"
                            for elem in data_set_config["import_config"].get(
                                "mapping_from_file", []
                            )
                        ]
                        + csvreader.fieldnames
                    )

                    with open(
                        data_set_config["file_path"] + "_enriched.csv", "w"
                    ) as output_file:
                        csvwriter = csv.DictWriter(output_file, fieldnames=fieldnames)
                        csvwriter.writeheader()

                        for index, row in enumerate(csvreader):
                            print(row)
                            # time.sleep(1)
                            place_dict = create_place_dict(
                                row, data_set_config["import_config"]
                            )
                            row_enriched = {**dict(row), **place_dict}
                            print(row_enriched)
                            csvwriter.writerow(row_enriched)
