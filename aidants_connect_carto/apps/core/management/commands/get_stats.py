# flake8: noqa

import csv
import time
import pandas as pd
import numpy as np

from django.core.management import BaseCommand

# from aidants_connect_carto import constants
# from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import Place, Service

HUB_LIST = ["Hub Siilabe", "Hub du Sud"]


def place_stats():
    print("=== Places ===")

    place_df = pd.DataFrame.from_records(Place.objects.all().values())
    place_df = place_df.replace("", np.nan)
    print(place_df.info())

    for hub in HUB_LIST:
        print(f"=== Places > {hub} ===")
        place_hub_df = pd.DataFrame.from_records(
            Place.objects.filter(data_source=hub).values()
        )
        place_hub_df = place_hub_df.replace("", np.nan)
        print(place_hub_df.info())


def service_stats():
    print("=== Services ===")

    service_df = pd.DataFrame.from_records(Service.objects.all().values())
    service_df = service_df.replace("", np.nan)
    print(service_df.info())


class Command(BaseCommand):
    """
    python manage.py get_stats
    """

    help = "Get database stats"

    def handle(self, *args, **kwargs):
        place_stats()
        service_stats()
