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
    name = models.CharField(max_length=300, help_text="Le nom du lieu")
    description = models.TextField(blank=True, help_text="Une description du lieu")
    type = models.CharField(
        max_length=32,
        choices=TYPE_CHOICES,
        default=CHOICE_OTHER,
        help_text="La typologie du lieu",
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=CHOICE_OTHER,
        help_text="Le statut du lieu",
    )

    # --- location
    address_raw = models.CharField(max_length=300, help_text="L'adresse complète")
    address_housenumber = models.CharField(
        max_length=5,
        blank=True,
        help_text="Le numéro avec indice de répétition éventuel (bis, ter, A, B)",
    )
    address_street = models.CharField(
        max_length=150, blank=True, help_text="Le nom de la rue"
    )
    address_postcode = models.CharField(
        max_length=5, blank=True, help_text="Le code postal"
    )
    address_citycode = models.CharField(
        max_length=5, blank=True, help_text="Le code INSEE de la commune"
    )
    address_city = models.CharField(
        max_length=150, blank=True, help_text="Le nom de la commune"
    )
    # address_context = models.CharField(
    #     max_length=150, help_text="n° de département, nom de département et de région"
    # )
    latitude = models.FloatField(
        blank=True, null=True, help_text="La latitude (coordonnée géographique)"
    )
    longitude = models.FloatField(
        blank=True, null=True, help_text="La longitude (coordonnée géographique)"
    )
    is_itinerant = models.BooleanField(
        default=False, help_text="Le lieu est-il itinérant ?"
    )

    # --- contact
    contact_phone_raw = models.CharField(
        max_length=300, help_text="Le numéro de téléphone brut"
    )
    phone_regex = RegexValidator(
        regex=r"^[0-9]{10}$",
        message="le numéro de téléphone doit être au format 0123456789",
    )
    contact_phone = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[phone_regex],
        help_text="Le numéro de téléphone",
    )
    # contact_phone_international = models.CharField(help_text="") # regex="^[0-9]+$"
    contact_email = models.EmailField(
        max_length=150, blank=True, help_text="Le courriel"
    )
    contact_website = models.URLField(
        max_length=300, blank=True, help_text="L'adresse du site internet"
    )

    # --- opening hours
    # opening_hours = django-openinghours package ? JsonField ? custom Field ?
    opening_hours_raw = models.TextField(
        blank=True, help_text="Les horaires d'ouverture"
    )
    opening_hours_osm_format = models.CharField(
        max_length=150,
        blank=True,
        help_text="Les horaires d'ouverture au format OpenStreetMap",
    )

    # --- equipments
    # equipments = ArrayField() # EQUIPMENT_CHOICES
    has_equipment_wifi = models.BooleanField(default=False, help_text="WiFi")
    has_equipment_computer = models.BooleanField(default=False, help_text="Ordinateur")
    has_equipment_scanner = models.BooleanField(default=False, help_text="Scanner")
    has_equipment_printer = models.BooleanField(default=False, help_text="Imprimante")
    equipment_other = models.CharField(
        max_length=300, blank=True, help_text="Autres équipements disponibles"
    )

    # --- accessibility
    # accessibility = ArrayField(
    #     models.CharField(max_length=32, blank=True, choices=HANDICAP_CHOICES),
    #     default=list,
    #     blank=True,
    #     help_text="Accessible aux formes de handicap suivantes"
    # )
    has_accessibility_hi = models.BooleanField(
        default=False, help_text="Handicap auditif"
    )
    # has_accessibility_mei = models.BooleanField(
    #     default=False, help_text="Handicap mental"
    # )
    has_accessibility_mi = models.BooleanField(
        default=False, help_text="Handicap moteur"
    )
    has_accessibility_pi = models.BooleanField(
        default=False, help_text="Handicap intellectuel ou psychique"
    )
    has_accessibility_vi = models.BooleanField(
        default=False, help_text="Handicap visuel"
    )

    # --- languages
    # languages = ArrayField(
    #     models.CharField(max_length=32, blank=True, choices=LANGUAGE_CHOICES),
    #     default=list,
    #     blank=True,
    #     help_text="Langues parlées"
    # )
    languages = models.CharField(
        max_length=150, blank=True, help_text="Langues parlées"
    )

    # --- payment
    payment_methods = models.CharField(
        max_length=150, blank=True, help_text="Les moyens de paiement"
    )  # PAYMENT_CHOICES

    # --- other
    additional_information = JSONField(blank=True, null=True)

    # --- links to other databases
    osm_node_id = models.IntegerField(
        blank=True, null=True, help_text="OpenStreetMap node id"
    )

    # --- timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    name = models.CharField(max_length=300, help_text="Le nom du service")
    description = models.TextField(blank=True, help_text="Une description du service")
    place = models.ForeignKey(
        Place, null=False, on_delete=models.CASCADE, related_name="services"
    )
    siret = models.CharField(
        max_length=14, blank=True, help_text="Coordonnées juridiques (SIRET)"
    )  # regex="^[0-9]$"

    # --- support
    public_target = ArrayField(
        models.CharField(max_length=32, blank=True, choices=PUBLIC_CHOICES),
        default=list,
        blank=True,
        help_text="Public cible",
    )
    support_access = models.CharField(
        max_length=32,
        blank=True,
        choices=SUPPORT_ACCESS_CHOICES,
        help_text="Modalités d'accès",
    )  # multiple choices
    support_mode = models.CharField(
        max_length=32,
        blank=True,
        choices=SUPPORT_MODE_CHOICES,
        help_text="Modalités d'accompagnement",
    )  # multiple choices

    # --- schedule
    # schedule_hours = django-openinghours package ? JsonField ? custom Field ?
    schedule_hours_raw = models.TextField(
        blank=True,
        help_text="Les horaires du service (s'ils sont différents "
        "des horaires du lieu)",
    )
    schedule_hours_osm_format = models.CharField(
        max_length=150,
        blank=True,
        help_text="Les horaires du service au format OpenStreetMap",
    )

    # --- payment
    is_free = models.BooleanField(default=True, help_text="Le service est-il gratuit ?")
    price_detail = models.TextField(blank=True, help_text="Le details des prix")
    payment_methods = models.CharField(
        max_length=150,
        blank=True,
        help_text="Les moyens de paiements spécifiques à ce service",
    )  # PAYMENT_CHOICES

    # --- labels
    # label_aptic = # ManyToManyField ?
    has_label_aidants_connect = models.BooleanField(
        default=False, help_text="Labelisé Aidants Connect"
    )
    has_label_mfs = models.BooleanField(
        default=False, help_text="Labelisé France Service"
    )
    label_other = models.CharField(
        max_length=300, blank=True, help_text="Autres labels"
    )

    # --- other
    additional_information = JSONField(blank=True, null=True)

    # --- timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"
