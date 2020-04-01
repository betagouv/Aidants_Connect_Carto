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

    ## basics
    name = models.CharField(max_length=300, help_text="Le nom du lieu")

    ## location
    address_raw = models.CharField(max_length=300, help_text="L'adresse brute, complète")
    address_housenumber = models.CharField(max_length=5, help_text="Le numéro avec indice de répétition éventuel (bis, ter, A, B)")
    address_street = models.CharField(max_length=150, help_text="Le nom de la rue")
    address_postcode = models.CharField(max_length=5, help_text="Le code postal")
    address_citycode = models.CharField(max_length=5, help_text="Le code INSEE de la commune")
    address_city = models.CharField(max_length=150, help_text="Le nom de la commune")
    # address_context = models.CharField(max_length=150, help_text="n° de département, nom de département et de région")
    latitude = models.FloatField(help_text="La latitude (coordonnée géographique)")
    longitude = models.FloatField(help_text="La latitude (coordonnée géographique)")
    itinerant = models.BooleanField(default=False, help_text="Le lieu est-il itinérant ?")
    
    ## contact
    contact_email = models.EmailField(max_length=150, help_text="Le courriel")
    phone_regex = RegexValidator(regex=r"^[0-9]$", message="le numéro de téléphone doit être au format 0123456789")
    contact_phone = models.CharField(max_length=10, validators=[phone_regex], help_text="Le numéro de téléphone")
    # contact_phone_international = models.CharField(help_text="") # regex="^[0-9]+$"
    contact_website = models.EmailField(max_length=150, help_text="L'adresse du site internet")
    
    ## opening hours
    opening_hours_raw = models.CharField(max_length=150, help_text="Les horaires d'ouverture")
    # opening_hours = django-openinghours package ? JsonField ? custom Field ?
    
    ## payment
    payment_methods = models.CharField(max_length=150, help_text="Les moyens de paiement") # PAYMENT_CHOICES
    
    ## accessibility
    # accessibility = ArrayField(
    #     models.CharField(max_length=32, blank=True, choices=HANDICAP_CHOICES),
    #     default=list,
    #     blank=True,
    #     help_text="Accessible aux formes de handicap suivantes"
    # )
    accessibility_hi = models.BooleanField(default=False, help_text="Handicap auditif")
    accessibility_mi = models.BooleanField(default=False, help_text="Handicap moteur")
    accessibility_pi = models.BooleanField(default=False, help_text="Handicap intellectuel ou psychique")
    accessibility_vi = models.BooleanField(default=False, help_text="Handicap visuel")

    ## languages
    # languages = ArrayField(
    #     models.CharField(max_length=32, blank=True, choices=LANGUAGE_CHOICES),
    #     default=list,
    #     blank=True,
    #     help_text="Langues parlées"
    # )
    languages = models.CharField(max_length=150, help_text="Langues parlées")

    ## equipements
    # equipements = ArrayField() # EQUIPEMENT_CHOICES
    equipement_wifi = models.BooleanField(default=False, help_text="WiFi")
    equipement_computer = models.BooleanField(default=False, help_text="Ordinateur")
    equipement_scanner = models.BooleanField(default=False, help_text="Scanner")
    equipement_printer = models.BooleanField(default=False, help_text="Imprimante")
    equipement_other = models.CharField(max_length=300, help_text="Autres équipements disponibles")

    ## links to other databases
    osm_node_id = models.IntegerField(help_text="OpenStreetMap node id")
    
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

    ## basics
    description = models.TextField(default="No description provided")
    place = models.ForeignKey(
        Place, null=False, on_delete=models.CASCADE, related_name="services"
    )
    siret = models.CharField(max_length=14, help_text="Coordonnées juridiques") # regex="^[0-9]$"
    
    ## support
    public_target = ArrayField(
        models.CharField(max_length=32, blank=True, choices=PUBLIC_CHOICES),
        default=list,
        blank=True,
        help_text=""
    )
    support_mode = models.CharField(max_length=32, choices=SUPPORT_CHOICES, help_text="Modalités d'accompagnement")

    ## schedule
    schedule_hours_raw = models.CharField(max_length=150, help_text="Les horaires du service")
    # schedule_hours = django-openinghours package ? JsonField ? custom Field ?
    
    ## payment
    price_free = models.BooleanField(default=True, help_text="Le service est-il gratuit ?")
    price_detail = models.CharField(max_length=150, help_text="Le details des prix")
    payment_methods = models.CharField(max_length=150, help_text="Les moyens de paiements spécifiques à ce service") # PAYMENT_CHOICES
    
    ## labels
    # label_aptic = # ManyToManyField ?
    label_aidants_connect = models.BooleanField(default=False, help_text="Labelisé Aidants Connect")
    label_mfs = models.BooleanField(default=False, help_text="Labelisé France Service")
    label_other = models.CharField(max_length=300, help_text="Autres labels")
    
    ## timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
