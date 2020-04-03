from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator


class Place(models.Model):
    LANGUAGE_CHOICES = [
        ("fr", "Français"),
        ("en", "Anglais"),
        ("sl", "Language des signes"),
    ]
    EQUIPEMENT_CHOICES = [
        ("wifi", "WiFi"),
        ("ordinateur", "Ordinateur"),
        ("scanner", "Scanner"),
        ("imprimante", "Imprimante"),
        # "Autre"
    ]
    HANDICAP_CHOICES = [
        ("handicap moteur", "Handicap moteur"),
        ("handicap visuel", "Handicap visuel"),
        ("handicap auditif", "Handicap auditif"),
        ("handicap mental", "Handicap intellectuel ou psychique"),
        # "Maladie invalidante",
        # "Mobilité limitée"
    ]
    PAYMENT_CHOICES = [
        ("especes", "Espèces"),
        ("carte bancaire", "Carte bancaire"),
        ("cheque", "Chèque"),
        ("aptic", "Chèque APTIC"),
        ("cif", "Congé individuel de formation (CIF)"),
        # "CRP",
        # "AFPE"
    ]

    FORM_READONLY_FIELDS = (
        "address_housenumber", "address_street", "address_postcode", "address_citycode", "address_city",
        "latitude", "longitude",
        "osm_node_id",
    )

    ## basics
    name = models.CharField(max_length=300, help_text="Le nom du lieu")

    ## location
    address_raw = models.CharField(max_length=300, help_text="L'adresse complète")
    address_housenumber = models.CharField(max_length=5, blank=True, help_text="Le numéro avec indice de répétition éventuel (bis, ter, A, B)")
    address_street = models.CharField(max_length=150, blank=True, help_text="Le nom de la rue")
    address_postcode = models.CharField(max_length=5, blank=True, help_text="Le code postal")
    address_citycode = models.CharField(max_length=5, blank=True, help_text="Le code INSEE de la commune")
    address_city = models.CharField(max_length=150, blank=True, help_text="Le nom de la commune")
    # address_context = models.CharField(max_length=150, help_text="n° de département, nom de département et de région")
    latitude = models.FloatField(blank=True, null=True, help_text="La latitude (coordonnée géographique)")
    longitude = models.FloatField(blank=True, null=True, help_text="La latitude (coordonnée géographique)")
    is_itinerant = models.BooleanField(default=False, help_text="Le lieu est-il itinérant ?")
    
    ## contact
    phone_regex = RegexValidator(regex=r"^[0-9]$", message="le numéro de téléphone doit être au format 0123456789")
    contact_phone = models.CharField(max_length=10, blank=True, validators=[phone_regex], help_text="Le numéro de téléphone")
    # contact_phone_international = models.CharField(help_text="") # regex="^[0-9]+$"
    contact_email = models.EmailField(max_length=150, blank=True, help_text="Le courriel")
    contact_website = models.URLField(max_length=150, blank=True, help_text="L'adresse du site internet")
    
    ## opening hours
    opening_hours_raw = models.CharField(max_length=150, blank=True, help_text="Les horaires d'ouverture")
    # opening_hours = django-openinghours package ? JsonField ? custom Field ?
    
    ## equipements
    # equipements = ArrayField() # EQUIPEMENT_CHOICES
    has_equipement_wifi = models.BooleanField(default=False, help_text="WiFi")
    has_equipement_computer = models.BooleanField(default=False, help_text="Ordinateur")
    has_equipement_scanner = models.BooleanField(default=False, help_text="Scanner")
    has_equipement_printer = models.BooleanField(default=False, help_text="Imprimante")
    equipement_other = models.CharField(max_length=300, blank=True, help_text="Autres équipements disponibles")

    ## accessibility
    # accessibility = ArrayField(
    #     models.CharField(max_length=32, blank=True, choices=HANDICAP_CHOICES),
    #     default=list,
    #     blank=True,
    #     help_text="Accessible aux formes de handicap suivantes"
    # )
    has_accessibility_hi = models.BooleanField(default=False, help_text="Handicap auditif")
    has_accessibility_mi = models.BooleanField(default=False, help_text="Handicap moteur")
    has_accessibility_pi = models.BooleanField(default=False, help_text="Handicap intellectuel ou psychique")
    has_accessibility_vi = models.BooleanField(default=False, help_text="Handicap visuel")

    ## languages
    # languages = ArrayField(
    #     models.CharField(max_length=32, blank=True, choices=LANGUAGE_CHOICES),
    #     default=list,
    #     blank=True,
    #     help_text="Langues parlées"
    # )
    languages = models.CharField(max_length=150, blank=True, help_text="Langues parlées")

    ## payment
    payment_methods = models.CharField(max_length=150, blank=True, help_text="Les moyens de paiement") # PAYMENT_CHOICES

    ## links to other databases
    osm_node_id = models.IntegerField(blank=True, null=True, help_text="OpenStreetMap node id")
    
    ## timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Service(models.Model):
    PUBLIC_CHOICES = [
        ("tout public", "Tout public"),
        ("-25 ans", "-25 ans"),
        ("senior", "Sénior"),
        ("demandeur emploi", "Demandeur d'emploi"),
        ("famille", "Famille"),
    ]
    SUPPORT_CHOICES = [
        ("libre", "Libre"),
        ("individuel", "Individuel"),
        ("collectif", "Collectif"),
    ]

    FORM_READONLY_FIELDS = (

    )

    ## basics
    name = models.CharField(max_length=300, help_text="Le nom du service")
    description = models.TextField(help_text="Une description du service")
    place = models.ForeignKey(
        Place, null=False, on_delete=models.CASCADE, related_name="services"
    )
    siret = models.CharField(max_length=14, blank=True, help_text="Coordonnées juridiques (SIRET)") # regex="^[0-9]$"
    
    ## support
    public_target = ArrayField(
        models.CharField(max_length=32, blank=True, choices=PUBLIC_CHOICES),
        default=list,
        blank=True,
        help_text="Public cible"
    )
    support_mode = models.CharField(max_length=32, choices=SUPPORT_CHOICES, help_text="Modalités d'accompagnement")

    ## schedule
    schedule_hours_raw = models.CharField(max_length=150, blank=True, help_text="Les horaires du service")
    # schedule_hours = django-openinghours package ? JsonField ? custom Field ?
    
    ## payment
    is_free = models.BooleanField(default=True, help_text="Le service est-il gratuit ?")
    price_detail = models.CharField(max_length=150, blank=True, help_text="Le details des prix")
    payment_methods = models.CharField(max_length=150, blank=True, help_text="Les moyens de paiements spécifiques à ce service") # PAYMENT_CHOICES
    
    ## labels
    # label_aptic = # ManyToManyField ?
    has_label_aidants_connect = models.BooleanField(default=False, help_text="Labelisé Aidants Connect")
    has_label_mfs = models.BooleanField(default=False, help_text="Labelisé France Service")
    label_other = models.CharField(max_length=300, blank=True, help_text="Autres labels")
    
    ## timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
