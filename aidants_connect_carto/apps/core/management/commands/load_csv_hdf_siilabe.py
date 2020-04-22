# flake8: noqa

import csv
import time

from django.core.management import BaseCommand

from aidants_connect_carto import constants

from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import Place, Service


def create_place(row):
    print("in place")
    place = Place()

    place.name = row["Nom SP"]

    type_value = utilities.find_verbose_choice(
        constants.PLACE_TYPE_CHOICES, row["Nature"]
    )
    if type_value:
        place.type = type_value

    status_value = utilities.find_verbose_choice(
        constants.PLACE_STATUS_CHOICES, row["Statut"]
    )
    if status_value:
        place.status = status_value

    place.address_raw = " ".join([row["Adresse SP"], row["CP"], row["Commune"]])
    address_api_results = utilities.call_ban_address_search_api(place.address_raw)
    address_api_results_processed = utilities.process_ban_address_search_results(
        address_api_results
    )
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

    place.latitude = utilities.process_float(row["Latitude"])
    place.longitude = utilities.process_float(row["Longitude"])

    place.contact_phone_raw = row["Tél SP"]
    place.contact_phone = utilities.process_phone_number(row["Tél SP"])
    place.contact_email = row["Mail SP"]
    place.contact_website = row["Site SP"]

    place.opening_hours_raw = row["Ouverture"]
    if row["Ouverture"]:
        opening_hours_raw_processed = utilities.process_opening_hours(row["Ouverture"])
        try:
            place.opening_hours_osm_format = utilities.sanitize_opening_hours_with_hoh(
                opening_hours_raw_processed
            )
        except:  # noqa
            pass

    place.target_audience_raw = row["Publics"]
    place.target_audience = utilities.process_target_audience(place.target_audience_raw)

    place.additional_information = {
        "id": row["ID Exporter les données"],
        "epn": row["EPN"],
        "horodateur": row["Horodateur"],
        "public_specifique": row["Publics spécifiques"],
        "connaissance_aptic": row["connaissance aptic"],
        "interessee_aptic": row["intéréssée aptic"],
        "pmr": row["PMR"],
        "transports_en_commun": row["Transports en commun"],
        "collaboration": row["Collaboration"],
        "autres_structures_partenaires": row["Autres structures partenaires"],
        "autres_offres": row["Autres offres"],
        "cheques_aptic": row["chéques APTIC"],
        "lien_picto_access": row["LIEN PICTO ACCES"],
    }  # Territoire, Quel territoire, ...

    place.save()
    print(row["ID Exporter les données"], "-->", place.id)
    return place


def create_service_equipement(row, place: Place):
    print("in service: acces équipement")
    service_equipement = Service()
    service_equipement.place_id = place.id
    service_equipement.name = "Accès à un équipement informatique"
    service_equipement.description = row["Type équipement"]
    service_equipement.support_access = utilities.process_support_access(
        row["Conditions accès équipement"]
    )
    service_equipement.is_free = utilities.process_cost(row["Coût accès équipement"])
    service_equipement.price_details = row["Coût accès équipement"]
    service_equipement.schedule_hours_raw = row["Horaires équipement"]
    if service_equipement.schedule_hours_raw:
        schedule_hours_raw_processed = utilities.process_opening_hours(
            service_equipement.schedule_hours_raw
        )
        try:
            service_equipement.schedule_hours_osm_format = utilities.sanitize_opening_hours_with_hoh(
                schedule_hours_raw_processed
            )
        except:  # noqa
            pass

    service_equipement.additional_information = {
        "support_access_raw": row["Conditions accès équipement"],
    }

    service_equipement.save()
    print(
        row["ID Exporter les données"], "-->", place.id, service_equipement.id,
    )


def create_service_mednum(row, place: Place):
    print("in service: mednum")

    service_mednum = Service()
    service_mednum.place_id = place.id
    service_mednum.name = "Acquisition de compétences numériques"
    service_mednum.description = row["Compétences médnum"]
    service_mednum.support_access = utilities.process_support_access(
        row["Conditions accès médnum"]
    )
    service_mednum.support_mode = utilities.process_support_mode(
        row["Accompagnement médnum"]
    )
    service_mednum.is_free = utilities.process_cost(row["Coût accès démarches"])
    service_mednum.price_details = row["Coût accès démarches"]
    service_mednum.schedule_hours_raw = row["Horaires médnum"]
    if service_mednum.schedule_hours_raw:
        schedule_hours_raw_processed = utilities.process_opening_hours(
            service_mednum.schedule_hours_raw
        )
        try:
            service_mednum.schedule_hours_osm_format = utilities.sanitize_opening_hours_with_hoh(
                schedule_hours_raw_processed
            )
        except:  # noqa
            pass

    service_mednum.additional_information = {
        "support_access_raw": row["Conditions accès médnum"],
        "support_mode_raw": row["Accompagnement médnum"],
        "frequence_mednum": row["Fréquence médnum"],
    }

    service_mednum.save()
    print(
        row["ID Exporter les données"], "-->", place.id, service_mednum.id,
    )


def create_service_demarches(row, place: Place):
    print("in service: demarches")

    service_demarches = Service()
    service_demarches.place_id = place.id
    service_demarches.name = "Accompagnement aux démarches administratives en ligne"
    service_demarches.description = row["Type démarches"]
    service_demarches.support_access = utilities.process_support_access(
        row["Conditions accès démarches"]
    )
    service_demarches.support_mode = utilities.process_support_mode(
        row["Accompagnement démarches"]
    )
    service_demarches.is_free = utilities.process_cost(row["Coût accès démarches"])
    service_demarches.schedule_hours_raw = row["Horaires démarches"]
    if service_demarches.schedule_hours_raw:
        schedule_hours_raw_processed = utilities.process_opening_hours(
            service_demarches.schedule_hours_raw
        )
        try:
            service_demarches.schedule_hours_osm_format = utilities.sanitize_opening_hours_with_hoh(
                schedule_hours_raw_processed
            )
        except:  # noqa
            pass

    service_demarches.additional_information = {
        "demarches_specifiques": row["Démarches spécifiques"],
        "frequence_demarches": row["Fréquence démarches"],
    }

    service_demarches.save()
    print(
        row["ID Exporter les données"], "-->", place.id, service_demarches.id,
    )


def create_service_stockage(row, place: Place):
    print("in service: stockage")

    service_stockage = Service()
    service_stockage.place_id = place.id
    service_stockage.name = "Stockage numérique sécurisé"
    service_stockage.is_free = utilities.process_cost(row["Coût stockage"])

    service_stockage.save()
    print(
        row["ID Exporter les données"], "-->", place.id, service_stockage.id,
    )


def create_service_vente(row, place: Place):
    print("in service: vente materiel")

    service_vente = Service()
    service_vente.place_id = place.id
    service_vente.name = "Vente de matériel informatique"
    service_vente.description = row["typé vente matériel"]

    service_vente.save()
    print(
        row["ID Exporter les données"], "-->", place.id, service_vente.id,
    )


class Command(BaseCommand):
    """
    python manage.py load_csv_hdf_siilabe --path data/siilab-hdf_export.csv
    """

    help = "Load a csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]

        with open(path, "rt") as f:
            reader = csv.DictReader(f, delimiter=",")
            # print(reader.fieldnames)

            for index, row in enumerate(reader):
                if index < 10:  # all
                    time.sleep(2)
                    place = create_place(row)

                    # Service 1: Accès à un équipement informatique
                    # Equipement à disposition, Condition, Coût, Horaires // Fixe mobile équipement, Lieu mobilité équipement
                    if row["Accès équipement"] == "Oui":
                        create_service_equipement(row, place)

                    # Service 2: Acquisition de compétences numériques
                    # Compétences numériques, Condition, Accompagnement, Coût, Fréquence, Horaires // Fixe mobile médnum, Lieu mobilité médnum
                    if row["Médnum"] == "Oui":
                        create_service_mednum(row, place)

                    # Service 3: Accompagnement aux démarches administratives en ligne
                    # Types de démarche, Condition, Accompagnement, Coût, Fréquence, Horaires // Fixe mobile démarches, Lieu mobilité démarches
                    if row["Démarches"] == "Oui":
                        create_service_demarches(row, place)

                    # Service 4: Stockage numérique sécurisé
                    if row["Stockage"] == "Oui":
                        create_service_stockage(row, place)

                    # Service 5: Vente de matériel informatique
                    if row["vente matériel"] == "Oui":
                        create_service_vente(row, place)
