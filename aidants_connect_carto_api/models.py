from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import RegexValidator

import humanized_opening_hours as hoh


class Place(models.Model):
    CHOICE_OTHER = "autre"
    TYPE_CHOICES = (
        ("centre social", "Centre social"),
        (
            "securite sociale",
            "Organisme de sécurité sociale (CAF, CPAM, CARSAT, MSA...)",
        ),
        ("tiers lieu", "Tiers-lieu & coworking, FabLab"),
        ("association", "Association"),
        ("maison quartier", "Maison de quartier"),
        ("pimms", "Point Information Médiation Multi Services (PIMMS)"),
        ("msap", "Maison de Service au Public (MSAP)"),
        ("bibliotheque", "Bibliothèque - Médiathèque"),
        ("formation", "Organisme de formations"),
        ("pole emploi", "Pôle Emploi"),
        ("commune", "Commune (Ville, CCAS, Centre Culturel...)"),
        ("intercommunalite", "Intercommunalité (EPCI)"),
        ("administration", "Administration - Collectivité territoriale"),
        ("departement", "Département (UTPAS, MDS, MDSI, UTAS...)"),
        ("prefecture", "Préfecture, Sous-Préfecture"),
        (CHOICE_OTHER, "Autre, Inconnu"),
    )
    STATUS_CHOICES = (
        ("public", "Public"),
        ("prive", "Privé"),
        ("public-prive", "Public / Privé"),
        (CHOICE_OTHER, "Autre, Inconnu"),
    )
    LANGUAGE_CHOICES = (
        ("fr", "Français"),
        ("en", "Anglais"),
        ("fsl", "Language des signes"),
    )
    EQUIPMENT_CHOICES = (
        ("wifi", "WiFi"),
        ("ordinateur", "Ordinateur"),
        ("scanner", "Scanner"),
        ("imprimante", "Imprimante"),
        # "Autre"
    )
    HANDICAP_CHOICES = (
        ("handicap moteur", "Handicap moteur"),
        ("handicap visuel", "Handicap visuel"),
        ("handicap auditif", "Handicap auditif"),
        ("handicap mental", "Handicap intellectuel ou psychique"),
        # "Maladie invalidante",
        # "Mobilité limitée"
    )
    PAYMENT_CHOICES = (
        ("especes", "Espèces"),
        ("carte bancaire", "Carte bancaire"),
        ("cheque", "Chèque"),
        ("aptic", "Chèque APTIC"),
        ("cif", "Congé individuel de formation (CIF)"),
        # "CRP",
        # "AFPE"
    )

    FORM_READONLY_FIELDS = (
        "address_housenumber",
        "address_street",
        "address_postcode",
        "address_citycode",
        "address_city",
        "latitude",
        "longitude",
        "osm_node_id",
    )

    # --- basics
    name = models.CharField(
        verbose_name="Le nom du lieu", max_length=300, help_text="BetaGouv"
    )
    description = models.TextField(
        verbose_name="Une description du lieu",
        blank=True,
        help_text="L'incubateur de Services Numériques de l'État",
    )
    type = models.CharField(
        verbose_name="La typologie du lieu",
        max_length=32,
        choices=TYPE_CHOICES,
        default=CHOICE_OTHER,
        help_text="Administration",
    )
    status = models.CharField(
        verbose_name="Le statut du lieu",
        max_length=32,
        choices=STATUS_CHOICES,
        default=CHOICE_OTHER,
        help_text="Public",
    )

    # --- location
    address_raw = models.CharField(
        verbose_name="L'adresse complète",
        max_length=300,
        help_text="20 Avenue de Ségur 75007 Paris",
    )
    address_housenumber = models.CharField(
        verbose_name="Le numéro avec indice de répétition éventuel (bis, ter, A, B)",
        max_length=5,
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
    # address_context = models.CharField(
    #     verbose_name="n° de département, nom de département et de région",
    #     max_length=150,
    #     help_text=""
    # )
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
    # contact_phone_international = models.CharField(help_text="") # regex="^[0-9]+$"
    contact_email = models.EmailField(
        verbose_name="Le courriel",
        max_length=150,
        blank=True,
        help_text="exemple@email.fr",
    )
    contact_website = models.URLField(
        verbose_name="L'adresse du site internet",
        max_length=300,
        blank=True,
        help_text="https://beta.gouv.fr/",
    )

    # --- opening hours
    # opening_hours = django-openinghours package ? JsonField ? custom Field ?
    opening_hours_raw = models.TextField(
        verbose_name="Les horaires d'ouverture",
        blank=True,
        help_text="Du lundi au vendredi de 8h à 20h",
    )
    opening_hours_osm_format = models.CharField(
        verbose_name="Les horaires d'ouverture au format OpenStreetMap",
        max_length=150,
        blank=True,
        help_text="Mo-Fr 8:00-20:00",
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

    # --- payment
    payment_methods = models.CharField(
        verbose_name="Les moyens de paiement",
        max_length=150,
        blank=True,
        help_text="Espèces, Carte Bancaire, ...",
    )  # PAYMENT_CHOICES

    # --- other
    additional_information = JSONField(
        verbose_name="Informations additionnelles stockées au format JSON",
        blank=True,
        null=True,
    )

    # --- links to other databases
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
        return self.services.values_list("name", flat=True)

    @property
    def opening_hours_description(self) -> list:
        """
        Transform opening_hours_osm_format into a readable description
        'Mo-Fr 8:00-20:00' --> ['Du lundi au vendredi : 08:00 – 20:00.']

        TODO: Store as model field ?
        """
        if not self.opening_hours_osm_format:
            return []

        oh = hoh.OHParser(self.opening_hours_osm_format, locale="fr")
        return oh.description()

    @property
    def opening_hours_week_description(self) -> list:
        """
        Transform `opening_hours_osm_format` into a list
        of readable descriptions per day.

        For example, if `opening_hours_osm_format` contains the string
        "Mo-Fr 8:00-20:00", this method returns the following output:
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
        if not self.opening_hours_osm_format:
            return []

        oh = hoh.OHParser(self.opening_hours_osm_format, locale="fr")
        return oh.plaintext_week_description().split("\n")

    @property
    def opening_hours_today(self) -> list:
        """Get the opening times of the current day.

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
        if not self.opening_hours_osm_format:
            return []

        oh = hoh.OHParser(self.opening_hours_osm_format, locale="fr")
        return oh.get_day().timespans

    @property
    def is_open(self) -> bool:
        """Return `True` if the `place` is currently open, or `False` otherwise."""
        if not self.opening_hours_osm_format:
            return False

        oh = hoh.OHParser(self.opening_hours_osm_format, locale="fr")
        return oh.is_open()


class Service(models.Model):
    PUBLIC_CHOICES = [
        ("tout public", "Tout public"),
        ("-25 ans", "-25 ans"),
        ("senior", "Sénior"),
        ("demandeur emploi", "Demandeur d'emploi"),
        ("famille", "Famille"),
    ]
    SUPPORT_ACCESS_CHOICES = [
        ("libre", "Accès libre"),
        ("inscription", "Sur inscription"),
        ("public cible", "Public cible uniquement"),
        ("adherents", "Adhérents uniquement"),
    ]
    SUPPORT_MODE_CHOICES = [
        ("individuel", "Individuel, Personnalisé"),
        ("collectif", "Collectif"),
    ]

    # FORM_READONLY_FIELDS = ("place_id")

    # --- basics
    name = models.CharField(verbose_name="Le nom du service", max_length=300)
    description = models.TextField(
        verbose_name="Une description du service", blank=True
    )
    place = models.ForeignKey(
        Place, null=False, on_delete=models.CASCADE, related_name="services"
    )
    siret = models.CharField(
        verbose_name="Coordonnées juridiques (SIRET)", max_length=14, blank=True
    )  # regex="^[0-9]$"

    # --- support
    public_target = ArrayField(
        verbose_name="Public cible",
        base_field=models.CharField(max_length=32, blank=True, choices=PUBLIC_CHOICES),
        default=list,
        blank=True,
    )
    support_access = models.CharField(
        verbose_name="Modalités d'accès",
        max_length=32,
        blank=True,
        choices=SUPPORT_ACCESS_CHOICES,
    )  # multiple choices
    support_mode = models.CharField(
        verbose_name="Modalités d'accompagnement",
        max_length=32,
        blank=True,
        choices=SUPPORT_MODE_CHOICES,
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

    # --- payment
    is_free = models.BooleanField(
        verbose_name="Le service est-il gratuit ?", default=True
    )
    price_detail = models.TextField(verbose_name="Le details des prix", blank=True)
    payment_methods = models.CharField(
        verbose_name="Les moyens de paiements spécifiques à ce service",
        max_length=150,
        blank=True,
    )  # PAYMENT_CHOICES

    # --- labels
    # label_aptic = # ManyToManyField ?
    has_label_aidants_connect = models.BooleanField(
        verbose_name="Labelisé Aidants Connect", default=False
    )
    has_label_mfs = models.BooleanField(
        verbose_name="Labelisé France Service", default=False
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
