# flake8: noqa

import csv
import time
import pandas as pd
import numpy as np

from django.core.management import BaseCommand

# from aidants_connect_carto import constants
# from aidants_connect_carto.apps.core import utilities
from aidants_connect_carto.apps.core.models import Place, Service, DataSource


def data_source_stats():
    print("=== Data Sources ===")
    sources = DataSource.objects.all()
    for source in sources:
        print(source.id, source.name, ">", "Places:", source.places.count())


def place_stats():
    print("=== Places ===")

    place_df = pd.DataFrame.from_records(Place.objects.all().values())
    place_df = place_df.replace("", np.nan)
    print(place_df.info())

    for source in DataSource.objects.all():
        print(f"=== Places > {source.name} ===")
        place_hub_df = pd.DataFrame.from_records(
            Place.objects.filter(data_source=source).values()
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
        data_source_stats()
        place_stats()
        service_stats()
