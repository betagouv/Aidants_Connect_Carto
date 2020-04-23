import re

from django.conf import settings

import humanized_opening_hours as hoh
import requests as python_request


# CHOICE fields


def find_verbose_choice(choices: list, value: str):
    for choice in choices:
        if choice[1] == value:
            return choice[0]
    # raise Exception(f"error with choices for {value}")
    return None


# Float fields


def process_float(value: str):
    if value:
        value = value.replace(",", ".")
        return float(value)
    return None


# Address


def process_address(address_string: str):
    """
    Call the BAN Address API
    Return the result depending on the score_threshold
    """
    address_api_results = call_ban_address_search_api(address_string)
    return _process_ban_address_search_results(address_api_results)


def call_ban_address_search_api(search_q_param: str):
    response = python_request.get(
        f"{settings.BAN_ADDRESS_SEARCH_API}?q={search_q_param}"
    )
    return response.json()


def _process_ban_address_search_results(results_json, score_threshold: int = 0.9):
    """
    https://geo.api.gouv.fr/adresse
    type: 'housenumber', 'street', 'locality' or 'municipality'
    example of type 'street': Place de la Gare 59460 Jeumont
    """
    if results_json["features"]:
        results_first_address = results_json["features"][0]
        if results_first_address["properties"]["score"] > score_threshold:
            # print(results_first_address)
            address_housenumber = (
                results_first_address["properties"]["housenumber"]
                if (results_first_address["properties"]["type"] == "housenumber")
                else ""
            )
            address_street = (
                results_first_address["properties"]["street"]
                if (results_first_address["properties"]["type"] == "housenumber")
                else results_first_address["properties"]["name"]
            )
            address_context = results_first_address["properties"]["context"]
            address_context_split = address_context.split(", ")
            return {
                "housenumber": address_housenumber,
                "street": address_street,
                "postcode": results_first_address["properties"]["postcode"],
                "citycode": results_first_address["properties"]["citycode"],
                "city": results_first_address["properties"]["city"],
                "departement_code": address_context_split[0],
                "departement_name": address_context_split[1],
                "region_name": address_context_split[2],
                "latitude": results_first_address["geometry"]["coordinates"][1],
                "longitude": results_first_address["geometry"]["coordinates"][0],
            }


# Phone number


def process_phone_number(phone_number_string: str):
    """
    Input: phone_number raw string
    Output: phone_number in 10 characters, empty string instead
    Examples:
    03 44 91 12 52
    03.23.52.24.05
    03-44-15-67-02
    3960 (Service 0,06 € / mn + prix appel)
    0810 25 59 80* (0,06 €/mn + prix appel)  Un conseiller vous répond du lundi au vendredi de 9h à 16h00. # noqa
    """
    phone_number_string_cleaned = (
        phone_number_string.replace(" ", "").replace(".", "").replace("-", "")
    )
    if len(phone_number_string_cleaned) <= 10:
        return phone_number_string_cleaned
    return ""


# Opening Hours


def process_opening_hours_to_osm_format(opening_hours_string: str):
    """
    Input: opening_hours raw string
    Output: opening_hours with osm format if correctly formated, empty string instead
    Exemples:
    "Du lundi au vendredi de 8h30 à 12h et de 14h à 17h30" --> "Mo-Fr 08:30-12:00,14:00-17:30" # noqa
    """
    if opening_hours_string:
        opening_hours_string_cleaned = _clean_opening_hours(opening_hours_string)
        try:
            return _sanitize_opening_hours_with_hoh(opening_hours_string_cleaned)
        except:  # noqa
            pass
    return ""


def _clean_opening_hours(opening_hours_string: str):
    """
    'Du lundi au vendredi : 09:00-12:00 et 14:00-16:30 / Samedi : 09:00-12:00'
    'Mo-Fr 09:00-12:00, 14:00-16:30 ; Sa 09:00-12:00'
    'du lundi au samedi matin'
    """
    # hoh.sanitize(opening_hours_string) ? https://github.com/rezemika/humanized_opening_hours/issues/38 # noqa
    opening_hours_string = opening_hours_string.replace("\xa0", " ")
    opening_hours_string = re.sub(" h ", ":", opening_hours_string, flags=re.IGNORECASE)
    # opening_hours_string = re.sub("h ", ":00 ", opening_hours_string, flags=re.IGNORECASE) # sanitize can take care of it # noqa
    opening_hours_string = re.sub(
        " au ", "-", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = opening_hours_string.replace(" à ", "-")
    opening_hours_string = re.sub(" et", ",", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = re.sub(
        " puis de", ",", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(" de", "", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = re.sub("le ", "", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = opening_hours_string.replace(" :", "")
    opening_hours_string = opening_hours_string.replace("/", ";")
    opening_hours_string = opening_hours_string.replace("–", "-")
    opening_hours_string = opening_hours_string.replace(" - ", "-")
    opening_hours_string = re.sub("du", "", opening_hours_string, flags=re.IGNORECASE)

    # fix sanitization errors (mo-fr 8h30-12h --> Mo-Fr 08:0030-12:00)
    opening_hours_string = re.sub(
        "h00", ":00", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "h15", ":15", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "h30", ":30", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "h45", ":45", opening_hours_string, flags=re.IGNORECASE
    )

    # day of weeks
    opening_hours_string = re.sub(
        "lundis", "Mo", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "lundi", "Mo", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "mardis", "Tu", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "mardi", "Tu", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "mercredis", "We", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "mercredi", "We", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "jeudis", "Th", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "jeudi", "Th", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "vendredis", "Fr", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "vendredi", "Fr", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "samedi", "Sa", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "samedis", "Sa", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "dimanches", "Su", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "dimanche", "Su", opening_hours_string, flags=re.IGNORECASE
    )
    return opening_hours_string.lower()


def process_service_schedule_hours(service_schedule_hours_string: str):
    """
    TODO: not used ?
    """
    if any(
        elem in service_schedule_hours_string.lower() for elem in ["de la structure"]
    ):
        return None
    return service_schedule_hours_string


def _sanitize_opening_hours_with_hoh(opening_hours: str):
    """
    https://github.com/rezemika/humanized_opening_hours#basic-methods

    Cleans up the opening_hours string
    Must be close to the OSM format
    Returns an Exception if it fails to parse/sanitize the string

    '  mo-su 09:30-20h;jan off' --> 'Mo-Su 09:30-20:00; Jan off'
    'Tu 14h-16h' --> 'Tu 14:00-16:00'
    """
    sanitized_opening_hours = hoh.sanitize(opening_hours)
    hoh.OHParser(sanitized_opening_hours, locale="fr")  # fails if given a wrong format
    return sanitized_opening_hours


# Other fields


def process_target_audience(value: str):
    """
    Tout public
    Demandeurs d'emploi
    Adhérents
    Séniors
    Assurés sociaux
    jeunes
    Jeunes entre 16 et 25 ans
    Enseignants, formateurs jeunesses, membres associatifs
    Allocataires CAF
    Familles allocataires avec quotient familial (QF) inférieur à 800
    """
    target_audience_list = []
    if any(elem in value.lower() for elem in ["public"]):
        target_audience_list.append("tout public")
    if any(elem in value.lower() for elem in ["jeune"]):
        target_audience_list.append("-25 ans")
    if any(
        elem in value.lower()
        for elem in ["senior", "sénior", "retraite", "retraité", "âgé"]
    ):
        target_audience_list.append("senior")
    if any(elem in value.lower() for elem in ["demandeurs d'emploi"]):
        target_audience_list.append("demandeur emploi")
    if any(elem in value.lower() for elem in ["allocataire", "minima"]):
        target_audience_list.append("allocataire")
    return target_audience_list


def process_support_access(value: str):
    """
    'accès en mairie aux heures d'ouverture et sur rendez vous'
    'Allocataires CAF'
    'Accès libre - accompagnement si besoin'
    'Accès libre / La consultation est limitée à 30 minutes par personne'
    'accès libre hors ateliers'
    """
    if any(elem in value.lower() for elem in ["libre"]):
        return "libre"
    if any(
        elem in value.lower()
        for elem in ["rdv", "rendez", "inscription", "réservation"]
    ):
        return "inscription"
    return ""


def process_support_mode(value: str):
    """
    'Accompagnement individuel et personnalisé'
    'accompagnement personnalisé sur demande'
    'Collectif et accompagnement individuel'
    'Individuel ou collectif'
    """
    if any(
        elem in value.lower() for elem in ["personnalisé", "individuel", "personnel"]
    ):
        return "individuel"
    if any(elem in value.lower() for elem in ["groupe", "collectif"]):
        return "collectif"
    return ""


def process_cost(value: str):
    """
    'Gratuit - Tarif d’adhésion annuelle : 6€'
    'Gratuit pour les habitants du Sud-Avesnois / abonnement annuel de 80 euros pour les personnes extérieures' # noqa
    """
    if value:
        if any(elem in value.lower() for elem in ["gratuit"]):
            return True
        if any(elem in value.lower() for elem in ["payant", "coût", "prix"]):
            return False
    return False
