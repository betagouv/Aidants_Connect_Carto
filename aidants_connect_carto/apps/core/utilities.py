import re

from django.conf import settings

import humanized_opening_hours as hoh
import requests as python_request

from aidants_connect_carto import constants


# CHOICE fields


def get_choice_verbose(choices: list, value: str):
    for choice in choices:
        if value == choice[0]:
            return choice[1]
    # raise Exception(f"error with choices for {value}")
    return None


# Float fields


def process_float(value: str):
    if value:
        value = value.replace(",", ".")
        return float(value)
    return None


# Boolean fields


def process_boolean(value: str, destination="db"):
    """
    Examples:
    ('oui', 'db') --> True
    ('oui', 'file') --> FILE_BOOLEAN_TRUE
    """
    if value:
        if any(elem in value.lower() for elem in ["oui", "vrai", "true"]):
            return True if (destination == "db") else constants.FILE_BOOLEAN_TRUE
    return False if (destination == "db") else constants.FILE_BOOLEAN_FALSE


def process_is_online(value: str, destination="db"):
    """
    """
    if value:
        return True if (destination == "db") else constants.FILE_BOOLEAN_TRUE
    return False if (destination == "db") else constants.FILE_BOOLEAN_FALSE


"""
Mapping to string:
- type
- status
- legal_entity_type
- service
"""


def process_type(value: str, destination="db"):
    """
    Output: 1 possible value, default to CHOICE_OTHER (or EMPTY_STRING)
    Examples:
    ('', 'db') --> CHOICE_OTHER
    ('', 'file') --> EMPTY_STRING
    """
    # init
    choices = constants.PLACE_TYPE_CHOICES
    mapping = constants.PLACE_TYPE_MAPPING
    output = None

    # match input value
    if value:
        for type_mapping_item in mapping:
            if value.strip().lower() in type_mapping_item[1].lower():
                output = type_mapping_item[0]

    # return
    if destination == "db":
        return output or constants.CHOICE_OTHER
    else:
        return get_choice_verbose(choices, output) or constants.EMPTY_STRING


def process_status(value: str, destination="db"):
    """
    Output: 1 possible value, default to CHOICE_OTHER (or EMPTY_STRING)
    """
    # init
    choices = constants.PLACE_STATUS_CHOICES
    mapping = constants.PLACE_STATUS_MAPPING
    output = None

    # match input value
    if value:
        for status_mapping_item in mapping:
            if value.strip().lower() == status_mapping_item[1].lower():
                output = status_mapping_item[0]

    # return
    if destination == "db":
        return output or constants.CHOICE_OTHER
    else:
        return get_choice_verbose(choices, output) or constants.EMPTY_STRING


def process_legal_entity_type(value: str, destination="db"):
    """
    Output: 1 possible value, default to CHOICE_OTHER (or EMPTY_STRING)
    """
    # init
    choices = constants.PLACE_LEGAL_ENTITY_TYPE_CHOICES
    mapping = constants.PLACE_LEGAL_ENTITY_TYPE_MAPPING
    output = None

    # match input value
    if value:
        for legal_entity_type_mapping_item in mapping:
            if value.strip().lower() in legal_entity_type_mapping_item[1].lower():
                output = legal_entity_type_mapping_item[0]

    # return
    if destination == "db":
        return output or constants.CHOICE_OTHER
    else:
        return get_choice_verbose(choices, output) or constants.EMPTY_STRING


def process_service_name(value: str, destination="db"):
    """
    Output: 1 possible value, default to EMPTY_STRING
    """
    # init
    choices = constants.SERVICE_NAME_CHOICES
    mapping = constants.SERVICE_NAME_MAPPING
    output = None

    # match input value
    if value:
        for service_name_mapping_item in mapping:
            if value.strip().lower() == service_name_mapping_item[1].lower():
                output = service_name_mapping_item[0]

    # return
    if destination == "db":
        return output or constants.EMPTY_STRING
    else:
        return get_choice_verbose(choices, output) or constants.EMPTY_STRING


"""
Mapping to list:
- target_audience
- support_access
- support_mode
- labels
"""


def process_target_audience(value: str, destination="db"):
    """
    """
    # init
    choices = constants.TARGET_AUDIENCE_CHOICES
    mapping = constants.TARGET_AUDIENCE_MAPPING
    output = []

    # match input value(s)
    if value:
        for target_audience_mapping_item in mapping:
            if any(elem in value.lower() for elem in target_audience_mapping_item[1]):
                output.append(target_audience_mapping_item[0])

    # return
    if destination == "db":
        return output
    else:
        return ",".join([get_choice_verbose(choices, elem) for elem in output])


def process_support_access(value: str, seperator=",", destination="db"):
    """
    """
    # init
    choices = constants.SUPPORT_ACCESS_CHOICES
    mapping = constants.SUPPORT_ACCESS_MAPPING
    output = []

    # match input value(s)
    if value:
        value_list = value.split(seperator)
        for value_item in value_list:
            for support_access_mapping_item in mapping:
                if value_item.strip().lower() in support_access_mapping_item[1].lower():
                    output.append(support_access_mapping_item[0])

    # return
    if destination == "db":
        return output
    else:
        return ",".join([get_choice_verbose(choices, elem) for elem in output])


def process_support_mode(value: str, seperator=",", destination="db"):
    """
    """
    # init
    choices = constants.SUPPORT_MODE_CHOICES
    mapping = constants.SUPPORT_MODE_MAPPING
    output = []

    # match input value(s)
    if value:
        value_list = value.split(seperator)
        for value_item in value_list:
            for support_mode_mapping_item in mapping:
                if value_item.strip().lower() in support_mode_mapping_item[1].lower():
                    output.append(support_mode_mapping_item[0])

    # return
    if destination == "db":
        return output
    else:
        return ",".join([get_choice_verbose(choices, elem) for elem in output])


def process_labels(value: str, seperator=",", destination="db"):
    """
    """
    # init
    choices = constants.LABEL_CHOICES
    mapping = constants.LABEL_MAPPING
    output = set()

    # match input value(s)
    if value:
        value_list = value.split(seperator)
        for value_item in value_list:
            for labels_mapping_item in mapping:
                if value_item.strip().lower() in labels_mapping_item[1].lower():
                    output.add(labels_mapping_item[0])

    # return
    output_sorted = sorted(list(output))
    if destination == "db":
        return output_sorted
    else:
        return ",".join([get_choice_verbose(choices, elem) for elem in output_sorted])


# Contact: Phone number


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


# Price details


def process_price(value: str):
    """
    'Gratuit - Tarif d’adhésion annuelle : 6€'
    'Gratuit pour les habitants du Sud-Avesnois / abonnement annuel de 80 euros pour les personnes extérieures' # noqa
    """
    if value:
        if any(elem in value.lower() for elem in ["gratuit"]):
            return True
        if any(elem in value.lower() for elem in ["payant", "coût", "prix"]):
            return False
    return True


# Address


def clean_address_raw_list(address: str, postcode: str, city: str):
    """
    Clean a bit the address_raw
    Why? To get better results from the BAN Address API
    """
    postcode = postcode.strip().zfill(5)
    address_raw = " ".join(
        [address.strip(), postcode, city.strip()]
    )  # city.strip().capitalize()
    return address_raw


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
    if ("features" in results_json) and len(results_json["features"]):
        results_first_address = results_json["features"][0]
        # if (len(results_json["features"]) == 1) or (results_first_address["properties"]["score"] > score_threshold): # noqa
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
            "region_name": address_context_split[2]
            if (len(address_context_split) > 2)
            else address_context_split[1],  # dom-tom # noqa
            "latitude": results_first_address["geometry"]["coordinates"][1],
            "longitude": results_first_address["geometry"]["coordinates"][0],
            "score": results_first_address["properties"]["score"],
        }
    else:
        return None


def get_address_full(
    address_housenumber: str,
    address_street: str,
    address_postcode: str,
    address_city: str,
) -> str:
    """
    20 Avenue de Ségur, 75007 Paris
    """
    return (
        f"{(address_housenumber + ' ') if address_housenumber else ''}"
        f"{address_street}"
        f"{', ' if (address_housenumber or address_street) else ''}"
        f"{(address_postcode + ' ') if address_postcode else ''}"
        f"{address_city}"
    )


# Opening Hours


def process_opening_hours_to_osm_format(opening_hours):
    """
    Input: opening_hours raw string (or list)
    Output: opening_hours with osm format if correctly formated, empty string instead
    Exemples:
    "Du lundi au vendredi de 8h30 à 12h et de 14h à 17h30" --> "Mo-Fr 08:30-12:00,14:00-17:30" # noqa
    """
    if opening_hours:
        # opening_hours is a list
        if type(opening_hours) == list:
            opening_hours_string = _clean_opening_hours_list(opening_hours)
        # opening_hours is a string
        elif " | " in opening_hours:
            opening_hours_string = _clean_opening_hours_list(opening_hours.split(" | "))
        elif "; " in opening_hours:
            opening_hours_string = _clean_opening_hours_list(opening_hours.split("; "))
        else:
            opening_hours_string = opening_hours

        opening_hours_string_cleaned = _clean_full_opening_hours(opening_hours_string)

        try:
            return _sanitize_opening_hours_with_hoh(opening_hours_string_cleaned)
        except:  # noqa
            pass
    return ""


def _clean_opening_hours_list(opening_hours_list: list):
    """
    Input: ["9:00 - 12:00 / 13:30 - 17:00", "10:00 - 13:00"]
    Output: "Mo 9:00-12:00,13:30-17:00; Tu 10:00-13:00"
    """
    MINIMUM_DAY_CHARS = 2
    # init
    opening_hours_list_cleaned = []
    days_list = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    # loop
    for index, elem in enumerate(opening_hours_list):
        if len(opening_hours_list[index]) > MINIMUM_DAY_CHARS:
            temp_opening_hours_day = (
                days_list[index]
                + " "
                + _clean_day_opening_hours(opening_hours_list[index])
            )
            opening_hours_list_cleaned.append(temp_opening_hours_day)
    return "; ".join(opening_hours_list_cleaned)


def _clean_day_opening_hours(opening_hours_string: str):
    """
    'Du lundi au vendredi : 09:00-12:00 et 14:00-16:30 / Samedi : 09:00-12:00'
    'Mo-Fr 09:00-12:00, 14:00-16:30 ; Sa 09:00-12:00'
    'du lundi au samedi matin'
    """
    # hoh.sanitize(opening_hours_string) ? https://github.com/rezemika/humanized_opening_hours/issues/38 # noqa
    opening_hours_string = opening_hours_string.replace("\xa0", " ").replace("\n", " ")
    opening_hours_string = re.sub(" h ", ":", opening_hours_string, flags=re.IGNORECASE)
    # opening_hours_string = re.sub("h ", ":00 ", opening_hours_string, flags=re.IGNORECASE) # sanitize can take care of it # noqa
    opening_hours_string = re.sub(
        " au ", "-", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(" à ", "-", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = re.sub(" et", ",", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = re.sub(
        " puis de", ",", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(" de", "", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = re.sub("le ", "", opening_hours_string, flags=re.IGNORECASE)
    opening_hours_string = opening_hours_string.replace(" :", "")
    opening_hours_string = opening_hours_string.replace(" / ", ",")  # seperates times
    opening_hours_string = opening_hours_string.replace("/", ",")  # seperates times
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
    # fix other sanitization errors
    opening_hours_string = re.sub(
        "9-", "9h-", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "9-", "9h-", opening_hours_string, flags=re.IGNORECASE
    )

    # off
    opening_hours_string = re.sub(
        "fermé", "off", opening_hours_string, flags=re.IGNORECASE
    )
    opening_hours_string = re.sub(
        "fermeture", "off", opening_hours_string, flags=re.IGNORECASE
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
    return opening_hours_string.lower().strip()


def _clean_full_opening_hours(opening_hours_string: str):
    # week/full specific rules
    opening_hours_string = opening_hours_string.replace(" / ", ";")  # seperates days
    # normal cleaning
    opening_hours_string = _clean_day_opening_hours(opening_hours_string)
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
    sanitized_opening_hours = hoh.sanitize(opening_hours.strip())
    hoh.OHParser(sanitized_opening_hours, locale="fr")  # fails if given a wrong format
    return sanitized_opening_hours


def get_opening_hours_osm_format_description(
    opening_hours_osm_format_string: str,
) -> list:
    """
    Transform opening_hours_osm_format into a readable description
    'Mo-Fr 08:00-20:00' --> ['Du lundi au vendredi : 08:00 – 20:00.']

    TODO: Store as model field ?
    """
    if not opening_hours_osm_format_string:
        return []

    oh = hoh.OHParser(opening_hours_osm_format_string, locale="fr")
    return oh.description()


def get_opening_hours_osm_format_week_description(
    opening_hours_osm_format_string: str,
) -> list:
    """
    Transform `opening_hours_osm_format` into a list
    of readable descriptions per day.

    For example, if `opening_hours_osm_format` contains the string
    "Mo-Fr 08:00-20:00", this method returns the following output:
    [
        'Lundi : 08:00 – 20:00',
        'Mardi : 08:00 – 20:00',
        'Mercredi : 08:00 – 20:00',
        'Jeudi : 08:00 – 20:00',
        'Vendredi : 08:00 – 20:00',
        'Samedi : fermé'
        'Dimanche : fermé'
    ]

    TODO: Store as model field ?
    """
    if not opening_hours_osm_format_string:
        return []

    oh = hoh.OHParser(opening_hours_osm_format_string, locale="fr")
    return oh.plaintext_week_description().split("\n")


def get_opening_hours_osm_format_today(opening_hours_osm_format_string: str) -> list:
    """
    Get the opening times of the current day.

    For example, if `opening_hours_osm_format` contains the string "Mo-Fr 8:00-20:00",
    this method returns the following output:
    [
        {
            'beginning': datetime.datetime(2020, 4, 8, 8, 0),
            'end': datetime.datetime(2020, 4, 8, 20, 0),
            'status': True,
            'timespan': <TimeSpan from ('normal', datetime.time(8, 0)) to ('normal', datetime.time(20, 0))>  # noqa
        }
    ]

    Usage: loop on results, then loop on timespan
    """
    if not opening_hours_osm_format_string:
        return []

    oh = hoh.OHParser(opening_hours_osm_format_string, locale="fr")
    return oh.get_day().timespans


def get_opening_hours_osm_format_is_open(opening_hours_osm_format_string: str) -> bool:
    """
    Return `True` if the `place` is currently open, or `False` otherwise.
    """
    if not opening_hours_osm_format_string:
        return False

    oh = hoh.OHParser(opening_hours_osm_format_string, locale="fr")
    return oh.is_open()
