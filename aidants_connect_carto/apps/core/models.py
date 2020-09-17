from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import RegexValidator

from aidants_connect_carto import constants
from aidants_connect_carto.apps.core import utilities


class DataSource(models.Model):
    # --- basics
    name = models.CharField(
        verbose_name="Le nom du fournisseur de donnée", max_length=300
    )
    description = models.TextField(
        verbose_name="Une description",
        blank=True,
        help_text="Plus de détails sur la source de donnée",
    )
    type = models.CharField(
        verbose_name="Le type de source",
        max_length=32,
        # choices=constants.DATA_SOURCE_TYPE_CHOICES,
        # default=constants.CHOICE_OTHER,
    )

    # --- contact
    contact_website_url = models.URLField(
        verbose_name="L'adresse du site internet de la source de donnée",
        max_length=300,
        blank=True,
    )

    # --- other
    logo_url = models.URLField(
        verbose_name="L'adresse du logo de la source de donnée",
        max_length=300,
        blank=True,
    )

    # --- dataset details
    dataset_name = models.CharField(
        verbose_name="Le nom du jeu de donnée", max_length=300
    )
    dataset_url = models.URLField(
        verbose_name="L'adresse où l'on peut trouver le jeu de donnée",
        max_length=300,
        blank=True,
    )
    dataset_local_path = models.CharField(
        verbose_name="Le chemin d'accès au jeu de donnée", max_length=300
    )
    dataset_last_updated = models.DateField(
        verbose_name="La date de dernière mise à jour du jeu de donnée",
        blank=True,
        null=True,
    )

    # --- import details
    import_config = JSONField(
        verbose_name="Information et configuration de l'import de la donnée",
        blank=True,
        null=True,
    )
    import_comment = models.TextField(
        verbose_name="Informations complémentaires sur l'import de la donnée",
        blank=True,
    )

    # --- timestamps
    created_at = models.DateTimeField(
        verbose_name="La date de création", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="La date de dernière modification", auto_now=True
    )

    class Meta:
        unique_together = ("name", "dataset_name")

    def __str__(self):
        return f"{self.name}: {self.dataset_name}"

    @property
    def place_count(self) -> int:
        return self.places.count()


class Place(models.Model):
    AUTO_POPULATED_FIELDS = [
        "address_housenumber",
        "address_street",
        "address_postcode",
        "address_citycode",
        "address_city",
        "address_departement_code",
        "address_departement_name",
        "address_region_name",
        "latitude",
        "longitude",
        "osm_node_id",
    ]

    # --- basics
    name = models.CharField(
        verbose_name="Le nom du lieu", max_length=300, help_text="BetaGouv"
    )
    supporting_structure_name = models.CharField(
        verbose_name="Le nom de la structure porteuse du lieu",
        blank=True,
        max_length=300,
        help_text="Services du Premier Ministre",
    )
    description = models.TextField(
        verbose_name="Une description du lieu",
        blank=True,
        help_text="L'incubateur de Services Numériques de l'État",
    )
    type = models.CharField(
        verbose_name="La typologie du lieu",
        max_length=32,
        choices=constants.PLACE_TYPE_CHOICES,
        default=constants.CHOICE_OTHER,
        help_text="Administration",
    )  # ArrayField (multiple choices) ?
    status = models.CharField(
        verbose_name="Le statut du lieu",
        max_length=32,
        choices=constants.PLACE_STATUS_CHOICES,
        default=constants.CHOICE_OTHER,
        help_text="Public",
    )
    legal_entity_type = models.CharField(
        verbose_name="La nature juridique du lieu",
        max_length=32,
        choices=constants.PLACE_LEGAL_ENTITY_TYPE_CHOICES,
        default=constants.CHOICE_OTHER,
        help_text="",
    )
    siret = models.CharField(
        verbose_name="Coordonnées juridiques (SIRET)", max_length=14, blank=True
    )

    # --- location
    address_raw = models.CharField(
        verbose_name="L'adresse complète",
        max_length=300,
        help_text="20 Avenue de Ségur 75007 Paris",
    )
    address_housenumber = models.CharField(
        verbose_name="Le numéro avec indice de répétition éventuel (bis, ter, A, B)",
        max_length=15,
        blank=True,
        help_text="20",
    )
    address_street = models.CharField(
        verbose_name="Le nom de la rue",
        max_length=150,
        blank=True,
        help_text="Avenue de Ségur",
    )
    address_postcode = models.CharField(
        verbose_name="Le code postal", max_length=5, blank=True, help_text="75007"
    )
    address_citycode = models.CharField(
        verbose_name="Le code INSEE de la commune",
        max_length=5,
        blank=True,
        help_text="75107",
    )
    address_city = models.CharField(
        verbose_name="Le nom de la commune",
        max_length=150,
        blank=True,
        help_text="Paris",
    )
    address_departement_code = models.CharField(
        verbose_name="Le numéro de département",
        max_length=3,
        blank=True,
        help_text="75",
    )
    address_departement_name = models.CharField(
        verbose_name="Le nom du département",
        max_length=150,
        blank=True,
        choices=constants.FRANCE_DEPARTEMENT_CHOICES,
        help_text="Paris",
    )
    address_region_name = models.CharField(
        verbose_name="Le nom de la région",
        max_length=150,
        blank=True,
        choices=zip(constants.FRANCE_REGION_LIST, constants.FRANCE_REGION_LIST),
        help_text="Île-de-France",
    )
    latitude = models.FloatField(
        verbose_name="La latitude (coordonnée géographique)",
        blank=True,
        null=True,
        help_text="48.850699",
    )
    longitude = models.FloatField(
        verbose_name="La longitude (coordonnée géographique)",
        blank=True,
        null=True,
        help_text="2.308628",
    )
    is_itinerant = models.BooleanField(
        verbose_name="Le lieu est-il itinérant ?", default=False
    )
    itinerant_details = models.TextField(
        verbose_name="Le details des déplacements", blank=True
    )
    is_online = models.BooleanField(
        verbose_name="Le lieu est-il uniquement en ligne ?", default=False
    )

    # --- contact
    contact_phone_raw = models.CharField(
        verbose_name="Le numéro de téléphone brut", max_length=300
    )
    phone_regex = RegexValidator(
        regex=r"^[0-9]{10}$",
        message="le numéro de téléphone doit être au format 0123456789",
    )
    contact_phone = models.CharField(
        verbose_name="Le numéro de téléphone",
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_regex],
        help_text="0123456789",
    )
    contact_phone_details = models.TextField(
        verbose_name="Le details du numéro de téléphone (horaires, prix, ...)",
        blank=True,
    )
    # contact_phone_international = models.CharField(help_text="") # regex="^[0-9]+$"
    contact_email = models.EmailField(
        verbose_name="Le courriel",
        max_length=150,
        blank=True,
        help_text="exemple@email.fr",
    )
    contact_website_url = models.URLField(
        verbose_name="L'adresse du site internet",
        max_length=300,
        blank=True,
        help_text="https://beta.gouv.fr/",
    )
    contact_facebook_url = models.URLField(
        verbose_name="L'adresse de la page Facebook", max_length=300, blank=True
    )
    contact_twitter_url = models.URLField(
        verbose_name="L'adresse de la page Twitter",
        max_length=300,
        blank=True,
        help_text="https://twitter.com/betagouv",
    )
    contact_youtube_url = models.URLField(
        verbose_name="L'adresse de la page Youtube", max_length=300, blank=True
    )

    # --- opening hours
    opening_hours_raw = models.TextField(
        verbose_name="Les horaires d'ouverture brut",
        blank=True,
        help_text="Du lundi au vendredi de 8h à 20h",
    )
    opening_hours_osm_format = models.CharField(
        verbose_name="Les horaires d'ouverture au format OpenStreetMap",
        max_length=150,
        blank=True,
        help_text="Mo-Fr 8:00-20:00",
    )
    opening_hours_details = models.TextField(
        verbose_name="Des détails supplémentaires sur les horaires d'ouverture",
        blank=True,
        help_text="sur rendez-vous le Mardi, porte-ouvertes le Mercredi, ...",
    )

    # --- equipments
    # equipments = ArrayField() # EQUIPMENT_CHOICES
    has_equipment_wifi = models.BooleanField(verbose_name="WiFi", default=False)
    has_equipment_computer = models.BooleanField(
        verbose_name="Ordinateur", default=False
    )
    has_equipment_scanner = models.BooleanField(verbose_name="Scanner", default=False)
    has_equipment_printer = models.BooleanField(
        verbose_name="Imprimante", default=False
    )
    equipment_other = models.CharField(
        verbose_name="Autres équipements disponibles", max_length=300, blank=True
    )

    # --- accessibility
    # accessibility = ArrayField(
    #     verbose_name="Accessible aux formes de handicap suivantes",
    #     base_field=models.CharField(
    #         max_length=32,
    #         blank=True,
    #         choices=HANDICAP_CHOICES
    #     ),
    #     default=list,
    #     blank=True
    # )
    has_accessibility_hi = models.BooleanField(
        verbose_name="Handicap auditif", default=False
    )
    # has_accessibility_mei = models.BooleanField(
    #     verbose_name="Handicap mental", default=False
    # )
    has_accessibility_mi = models.BooleanField(
        verbose_name="Handicap moteur", default=False
    )
    has_accessibility_pi = models.BooleanField(
        verbose_name="Handicap intellectuel ou psychique", default=False
    )
    has_accessibility_vi = models.BooleanField(
        verbose_name="Handicap visuel", default=False
    )

    # --- languages
    # languages = ArrayField(
    #     verbose_name="Langues parlées",
    #     base_field=models.CharField(
    #         max_length=32,
    #         blank=True,
    #         choices=LANGUAGE_CHOICES
    #     ),
    #     default=list,
    #     blank=True
    # )
    languages = models.CharField(
        verbose_name="Langues parlées",
        max_length=150,
        blank=True,
        help_text="Français, Anglais, ...",
    )

    # --- support
    target_audience_raw = models.TextField(
        verbose_name="Public(s) cible brut", blank=True
    )
    target_audience = ArrayField(
        verbose_name="Public(s) cible",
        base_field=models.CharField(
            max_length=32, blank=True, choices=constants.TARGET_AUDIENCE_CHOICES
        ),
        default=list,
        blank=True,
        help_text="tout public, jeune, senior, allocataire, etranger, ...",
    )
    support_access_raw = models.TextField(
        verbose_name="Modalité(s) d'accès brut", blank=True
    )
    support_access = ArrayField(
        verbose_name="Modalité(s) d'accès",
        base_field=models.CharField(
            max_length=32, blank=True, choices=constants.SUPPORT_ACCESS_CHOICES
        ),
        default=list,
        blank=True,
        help_text="libre, inscription, adherent, ...",
    )
    support_mode_raw = models.TextField(
        verbose_name="Modalité(s) d'accompagnement brut", blank=True
    )
    support_mode = ArrayField(
        verbose_name="Modalité(s) d'accompagnement",
        base_field=models.CharField(
            max_length=32, blank=True, choices=constants.SUPPORT_MODE_CHOICES
        ),
        default=list,
        blank=True,
        help_text="individuel, collectif, ...",
    )

    # --- price
    is_free = models.BooleanField(verbose_name="Le lieu est-il gratuit ?", default=True)
    price_details = models.TextField(
        verbose_name="Le details des prix du lieu", blank=True
    )
    payment_methods = models.CharField(
        verbose_name="Les moyens de paiement",
        max_length=150,
        blank=True,
        help_text="Espèces, Carte Bancaire, ...",
    )  # PAYMENT_CHOICES

    # --- labels
    has_label_fs = models.BooleanField(
        verbose_name="Labellisé France Service", default=False
    )

    # --- other
    logo_url = models.URLField(
        verbose_name="L'adresse du logo du lieu",
        max_length=300,
        blank=True,
        help_text="https://beta.gouv.fr/img/logo_twitter_image-2019.jpg",
    )
    additional_information = JSONField(
        verbose_name="Informations additionnelles stockées au format JSON",
        blank=True,
        null=True,
    )

    # --- links to other models & databases
    data_source = models.ForeignKey(
        DataSource,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="places",
    )
    osm_node_id = models.IntegerField(
        verbose_name="OpenStreetMap node id",
        blank=True,
        null=True,
        help_text="5266052428",
    )

    # --- timestamps
    created_at = models.DateTimeField(
        verbose_name="La date de création", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="La date de dernière modification", auto_now=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"

    @property
    def service_count(self) -> int:
        return self.services.count()

    @property
    def service_list(self) -> list():
        return list(self.services.values_list("name", flat=True))

    @property
    def display_address_full(self) -> str:
        """
        20 Avenue de Ségur, 75007 Paris
        """
        return utilities.get_address_full(
            self.address_housenumber,
            self.address_street,
            self.address_postcode,
            self.address_city,
        )

    @property
    def opening_hours_description(self) -> list:
        """
        Transform opening_hours_osm_format into a readable description
        'Mo-Fr 08:00-20:00' --> ['Du lundi au vendredi : 08:00 – 20:00.']

        TODO: Store as model field ?
        """
        return utilities.get_opening_hours_osm_format_description(
            self.opening_hours_osm_format
        )

    @property
    def opening_hours_week_description(self) -> list:
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
        return utilities.get_opening_hours_osm_format_week_description(
            self.opening_hours_osm_format
        )

    @property
    def opening_hours_today(self) -> list:
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
        """
        return utilities.get_opening_hours_osm_format_today(
            self.opening_hours_osm_format
        )

    @property
    def is_open(self) -> bool:
        """
        Return `True` if the `place` is currently open, or `False` otherwise.
        """
        return utilities.get_opening_hours_osm_format_is_open(
            self.opening_hours_osm_format
        )


class Service(models.Model):
    # AUTO_POPULATED_FIELDS = ("place_id")

    # --- basics
    name = models.CharField(
        verbose_name="Le nom du service", max_length=300
    )  # choices=zip(constants.SERVICE_NAME_LIST, constants.SERVICE_NAME_LIST)
    description = models.TextField(
        verbose_name="Une description du service", blank=True
    )
    siret = models.CharField(
        verbose_name="Coordonnées juridiques (SIRET)", max_length=14, blank=True
    )  # regex="^[0-9]$"

    # --- support
    target_audience = ArrayField(
        verbose_name="Public cible (s'il est différent du public cible du lieu)",
        base_field=models.CharField(
            max_length=32, blank=True, choices=constants.TARGET_AUDIENCE_CHOICES
        ),
        default=list,
        blank=True,
    )
    support_access = models.CharField(
        verbose_name="Modalités d'accès (si différent du lieu)",
        max_length=32,
        blank=True,
        choices=constants.SUPPORT_ACCESS_CHOICES,
        help_text="libre, inscription, adherent, ...",
    )  # multiple choices
    support_mode = models.CharField(
        verbose_name="Modalités d'accompagnement (si différent du lieu)",
        max_length=32,
        blank=True,
        choices=constants.SUPPORT_MODE_CHOICES,
        help_text="individuel, collectif, ...",
    )  # multiple choices

    # --- schedule
    # schedule_hours = django-openinghours package ? JsonField ? custom Field ?
    schedule_hours_raw = models.TextField(
        verbose_name="Les horaires du service "
        "(s'ils sont différents des horaires du lieu)",
        blank=True,
        help_text="Le mardi de 14h à 18h",
    )
    schedule_hours_osm_format = models.CharField(
        verbose_name="Les horaires du service au format OpenStreetMap",
        max_length=150,
        blank=True,
        help_text="Tu 14:00-18:00",
    )

    # --- price
    is_free = models.BooleanField(
        verbose_name="Le service est-il gratuit ?", default=True
    )
    price_details = models.TextField(
        verbose_name="Le details des prix du service", blank=True
    )
    payment_methods = models.TextField(
        verbose_name="Les moyens de paiements spécifiques à ce service", blank=True,
    )  # PAYMENT_CHOICES

    # --- labels
    # label_aptic = # ManyToManyField ?
    has_label_aidants_connect = models.BooleanField(
        verbose_name="Labellisé Aidants Connect", default=False
    )
    label_other = models.CharField(
        verbose_name="Autres labels", max_length=300, blank=True
    )

    # --- other
    additional_information = JSONField(
        verbose_name="Informations additionnelles stockées au format JSON",
        blank=True,
        null=True,
    )

    # --- links to other models & databases
    place = models.ForeignKey(
        Place, null=False, on_delete=models.CASCADE, related_name="services"
    )

    # --- timestamps
    created_at = models.DateTimeField(
        verbose_name="La date de création", auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="La date de dernière modification", auto_now=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"
