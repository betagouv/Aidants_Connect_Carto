HUBS = []

CHOICE_OTHER = "autre"

PLACE_TYPE_CHOICES = [
    ("centre social", "Centre social"),
    ("securite sociale", "Organisme de sécurité sociale (CAF, CPAM, CARSAT, MSA...)",),
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
]

PLACE_STATUS_CHOICES = [
    ("public", "Public"),
    ("prive", "Privé"),
    ("public-prive", "Public / Privé"),
    (CHOICE_OTHER, "Autre, Inconnu"),
]

PLACE_LEGAL_ENTITY_TYPE_CHOICES = [
    ("association", "Association"),
    ("collectivite", "Collectivité locale ou territoriale"),
    ("cae", "Coopérative d'Activités et d'Entrepreneur·es (CAE)"),
    ("epci", "Établissement public de coopération intercommunale (EPCI)"),
    ("sasu", "Société par actions simplifiée unipersonnelle (SASU)"),
    ("scic", "société coopérative d’intérêt collectif (SCIC)"),
    ("scop", "Société coopérative et participative (SCOP)"),
    ("spl", "Société publique locale (SPL)"),
    (CHOICE_OTHER, "Autre, Inconnu"),
]

TARGET_AUDIENCE_CHOICES = [
    ("tout public", "Tout public"),
    ("-25 ans", "-25 ans, Jeune"),
    ("senior", "Sénior"),
    ("demandeur emploi", "Demandeur d'emploi"),
    ("famille", "Famille"),
    ("allocataire", "Allocataires"),
]

LANGUAGE_CHOICES = [
    ("fr", "Français"),
    ("en", "Anglais"),
    ("fsl", "Language des signes"),
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

EQUIPMENT_CHOICES = [
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

SERVICE_SUPPORT_ACCESS_CHOICES = [
    ("libre", "Accès libre"),
    ("inscription", "Sur inscription ou rendez-vous"),
    ("public cible", "Public cible uniquement"),
    ("adherents", "Adhérents uniquement"),
]
SERVICE_SUPPORT_MODE_CHOICES = [
    ("individuel", "Individuel, Personnalisé"),
    ("collectif", "Collectif"),
]

FRANCE_REGIONS = [
    "Auvergne-Rhône-Alpes",
    "Bourgogne-Franche-Comté",
    "Bretagne",
    "Centre-Val de Loire",
    "Corse",
    "Grand Est",
    "Hauts-de-France",
    "Île-de-France",
    "Normandie",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Pays de la Loire",
    "Provence-Alpes-Côte d'Azur",
    "Guadeloupe",
    "Martinique",
    "Guyane",
    "La Réunion",
    "Mayotte",
]

FRANCE_DEPARTEMENTS = []
