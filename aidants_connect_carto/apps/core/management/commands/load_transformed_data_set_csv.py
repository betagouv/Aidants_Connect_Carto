import csv

from django.core.management import BaseCommand

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import DataSet, Place, Service


MAPPING_SCHEMA_DB_FILE_PATH = "schema/mapping_schema_db.csv"
DEFAULT_SEPARATEUR_DATA_SET = ","
DEFAULT_SEPARATEUR_CHAMPS_MULTIPLES = ","
DEFAULT_DATA_SET_EXTENSION = ".csv"


class Command(BaseCommand):
    """
    Usage:
    python manage.py load_transformed_data_set_csv data/hub_abc/import_config.csv
    """

    help = "Load a data set (csv file) into the database using the specified config"

    def add_arguments(self, parser):
        parser.add_argument(
            "config",
            help="Le chemin vers la configuration d'import du jeu de donnée",
            nargs=1,
            type=str,
        )

    def handle(self, *args, **kwargs):
        # init
        data_set_config_file_path = kwargs["config"][0]
        data_set_source_name = ""
        data_set_name = ""
        data_set_transformed_file_path = ""
        mapping_config = []

        # Open the mapping-schema-db file
        print("Step 1 : reading mapping file")
        with open(MAPPING_SCHEMA_DB_FILE_PATH) as f:
            csvreader = csv.DictReader(f)
            mapping_config = [dict(d) for d in csvreader]

        # Get data_set metadata
        print("Step 2 : reading data_set config file")
        with open(data_set_config_file_path) as f:
            csvreader = csv.DictReader(f)
            data_set_config = [dict(d) for d in csvreader]
            # data_set source
            data_set_source_name = next(
                d["fichier"] for d in data_set_config if d["modele"] == "_meta_source"
            )
            # data_set name
            data_set_name = next(
                d["fichier"] for d in data_set_config if d["modele"] == "_meta_nom"
            )
            # data_set path
            data_set_file_path = next(
                d["fichier"]
                for d in data_set_config
                if d["modele"] == "_meta_fichier_chemin"
            )
            # data_set_transformed path
            data_set_transformed_file_path = (
                data_set_file_path.split(DEFAULT_DATA_SET_EXTENSION)[0]
                + "_transformed"
                + DEFAULT_DATA_SET_EXTENSION
            )

        # Process each line of the data_set
        print("Step 3 : retrieve the data_set name in the DB")
        try:
            data_set = DataSet.objects.get(
                name=data_set_name, data_source__name=data_set_source_name
            )
        except:  # noqa
            print("Erreur : impossible de trouver le DataSet :", data_set_name)
            print("Verifiez qu'il a bien été créé dans la base de donnée")
            return

        # Process each line of the data_set
        print("Step 4 : import the data_set places in the DB")
        with open(data_set_transformed_file_path) as f:
            csvreader = csv.DictReader(f)
            print("... number of rows :", sum(1 for row in csvreader))
            # reset the csvreader, and skip header
            f.seek(0)
            next(f)
            for index, row_place in enumerate(csvreader):
                place = create_place(row_place, data_set, mapping_config)

                if ("services" in row_place) and row_place["services"]:
                    place_services_list = row_place["services"].split(
                        DEFAULT_SEPARATEUR_CHAMPS_MULTIPLES
                    )
                    for place_service in place_services_list:
                        create_service(place_service, place)

        print("Done !")


def create_place(row_place, data_set, mapping_config):
    place_dict = {}

    place_dict["data_set_id"] = data_set.id

    for index, row_field in enumerate(mapping_config):
        if row_field["modele_schema"] in row_place:
            if row_place[row_field["modele_schema"]]:
                if row_field["modele_db"] not in [
                    "service__name"
                ]:  # processed seperately
                    place_dict[row_field["modele_db"]] = row_place[
                        row_field["modele_schema"]
                    ]

    print(place_dict)

    # process CharFields (with choices)
    if "type" in place_dict:
        place_dict["type"] = utilities.get_choice_db(
            constants.PLACE_TYPE_CHOICES, place_dict["type"]
        )
    if "status" in place_dict:
        place_dict["status"] = utilities.get_choice_db(
            constants.PLACE_STATUS_CHOICES, place_dict["status"]
        )
    if "legal_entity_type" in place_dict:
        place_dict["legal_entity_type"] = utilities.get_choice_db(
            constants.PLACE_LEGAL_ENTITY_TYPE_CHOICES, place_dict["legal_entity_type"]
        )

    # process ArrayFields (with choices)
    if "target_audience" in place_dict:
        place_dict["target_audience"] = utilities.get_choices_db_from_string(
            constants.TARGET_AUDIENCE_CHOICES, place_dict["target_audience"]
        )
    if "support_access" in place_dict:
        place_dict["support_access"] = utilities.get_choices_db_from_string(
            constants.SUPPORT_ACCESS_CHOICES, place_dict["support_access"]
        )
    if "support_mode" in place_dict:
        place_dict["support_mode"] = utilities.get_choices_db_from_string(
            constants.SUPPORT_MODE_CHOICES, place_dict["support_mode"]
        )
    if "price" in place_dict:
        place_dict["price"] = utilities.get_choices_db_from_string(
            constants.PRICE_CHOICES, place_dict["price"]
        )
    if "labels" in place_dict:
        place_dict["labels"] = utilities.get_choices_db_from_string(
            constants.LABEL_CHOICES, place_dict["labels"]
        )
    if "accessibility" in place_dict:
        place_dict["accessibility"] = utilities.get_choices_db_from_string(
            constants.ACCESSIBILITY_CHOICES, place_dict["accessibility"]
        )

    # clean BooleanFields
    if "is_itinerant" in place_dict:
        place_dict["is_itinerant"] = utilities.process_is_itinerant(
            place_dict["is_itinerant"]
        )
    if "is_online" in place_dict:
        place_dict["is_online"] = utilities.process_is_online(place_dict["is_online"])

    place = Place.objects.create(**place_dict)
    # print(row["ID"], "-->", place.id)
    print("--> place :", place.id)
    return place


def create_service(service_name, place):
    service = Service.objects.create(place_id=place.id, name=service_name)
    print("--> service :", service.id)
