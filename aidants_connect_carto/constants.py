# flake8: noqa

CHOICE_OTHER = "autre"

DATA_SOURCE_TYPE_CHOICES = [
    ("hub", "Hub"),
    ("national", "National"),
    ("region", "Région"),
    ("departement", "Département"),
    (CHOICE_OTHER, "Autre, Inconnu"),
]

# TODO: Maison France Services as a tag instead of a type
PLACE_TYPE_CHOICES = [
    ("administration", "Administration - Collectivité territoriale"),
    ("association", "Association"),
    ("bibliotheque", "Bibliothèque - Médiathèque"),
    ("commune", "Commune (Ville, CCAS, Centre Culturel...)"),
    ("centre social", "Centre social"),
    ("departement", "Département (UTPAS, MDS, MDSI, UTAS...)"),
    ("epn", "Espace Public Numérique (EPN)"),
    ("formation", "Organisme de formations"),
    ("intercommunalite", "Intercommunalité (EPCI)"),
    ("la poste", "La Poste"),
    ("maison quartier", "Maison de quartier"),
    ("msap", "Maison de Service au Public (MSAP)"),
    ("pole emploi", "Pôle Emploi"),
    ("pimms", "Point Information Médiation Multi Services (PIMMS)"),
    ("prefecture", "Préfecture, Sous-Préfecture"),
    ("securite sociale", "Organisme de sécurité sociale (CAF, CPAM, CARSAT, MSA...)"),
    ("tiers lieu", "Tiers-lieu & coworking, FabLab"),
    (CHOICE_OTHER, "Autre, Inconnu"),
]

PLACE_TYPE_MAPPING = PLACE_TYPE_CHOICES + [
    ("bibliotheque", "Bibliothèque / Médiathèque"),
    ("centre social", "centre socio-culturel"),
    ("centre social", "centre socioculturel"),
    ("commune", "Commune (Mairie, CCAS, Centre Culturel, Centre Social...)"),
    ("maison quartier", "Structure associative de quartier"),
    ("tiers lieu", "Tiers-Lieux"),
    ("tiers lieu", "Fablab / Hackerspace"),
    ("tiers lieu", "Espace de coworking"),
]

# TODO: quid d'avoir l'info "Privé" seule ?
PLACE_STATUS_CHOICES = [
    ("public", "Public"),
    ("prive", "Privé"),
    ("public-prive", "Public / Privé"),
    (CHOICE_OTHER, "Autre, Inconnu"),
]

PLACE_STATUS_MAPPING = PLACE_STATUS_CHOICES + [
    ("public", "Public : Collectivité"),
    ("prive", "Privé à but lucratif (entreprises, auto-entrepreneurs, SCOP, SCIC...)"),
    ("prive", "Privé à but non lucratif (association, ONG...)"),
]

PLACE_LEGAL_ENTITY_TYPE_CHOICES = [
    ("association", "Association"),
    ("collectivite", "Collectivité locale ou territoriale"),
    ("cae", "Coopérative d'Activités et d'Entrepreneur·es (CAE)"),
    ("epci", "Établissement public de coopération intercommunale (EPCI)"),
    ("epic", "Établissement public à caractère industriel et commercial (EPIC)"),
    (
        "epscp",
        "Établissement public à caractère scientifique, culturel et professionnel (EPSCP)",
    ),
    ("gip", "Groupement d'intérêt public (GIP)"),
    ("sas", "Société par actions simplifiée (SAS)"),
    ("sarl", "Société à responsabilité limitée (SARL)"),
    ("sasu", "Société par actions simplifiée unipersonnelle (SASU)"),
    ("scic", "société coopérative d’intérêt collectif (SCIC)"),
    ("scop", "Société coopérative et participative (SCOP)"),
    ("spl", "Société publique locale (SPL)"),
    (CHOICE_OTHER, "Autre, Inconnu"),
]

PLACE_LEGAL_ENTITY_TYPE_MAPPING = PLACE_LEGAL_ENTITY_TYPE_CHOICES + [
    ("association", "association (délégation de service public)"),
    ("collectivite", "collectivite"),
    ("collectivite", "collectivité"),
    ("collectivite", "collectivite territoriale"),
    ("collectivite", "collectivité territoriale"),
    ("cae", "cae"),
    ("cae", "sas-cae"),
    ("epci", "epci"),
    ("epic", "epic (etablissement public à caractère industriel et commercial)"),
    ("epscp", "epscp"),
    ("gip", "gip (groupement d'intérêt public)"),
    ("sas", "sas"),
    ("sarl", "sarl"),
    ("sasu", "sasu"),
    ("scic", "scic"),
    ("scic", "sarl-scic"),
    ("scop", "scop"),
    ("spl", "spl"),
    ("spl", "societe publique locale"),
    (CHOICE_OTHER, "non déclaré"),
]

TARGET_AUDIENCE_CHOICES = [
    ("tout public", "Tout public"),
    ("allocataire", "Allocataires"),
    ("demandeur emploi", "Demandeurs d'emploi"),
    ("etranger", "Étrangers"),
    ("famille", "Familles"),
    ("jeune", "-25 ans, Jeunes"),
    ("handicap", "Personnes en situation de handicap"),
    ("senior", "Séniors"),
]

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
TARGET_AUDIENCE_MAPPING = [
    ("tout public", ["public"]),
    ("allocataire", ["allocataire", "minima", "rsa", "caf"]),
    ("demandeur emploi", ["demandeur", "emploi"]),
    ("etranger", ["etranger", "étranger", "étrangère"]),
    ("handicap", ["handicap"]),
    ("jeune", ["jeune", "moins de"]),
    ("senior", ["senior", "retraite", "retraité", "âgé", "plus de"]),
]

SUPPORT_ACCESS_CHOICES = [
    ("libre", "Accès libre"),
    ("inscription", "Sur inscription ou rendez-vous"),
    ("public cible", "Public cible uniquement"),
    ("adherent", "Adhérents uniquement"),
]

SUPPORT_ACCESS_MAPPING = SUPPORT_ACCESS_CHOICES + [
    ("libre", "sans rendez-vous"),
    ("libre", "ouvert à tous"),
    ("inscription", "prise de rendez-vous"),
    ("inscription", "sur rendez-vous"),
    ("inscription", "ouvert à tous sur réservation"),
    ("inscription", "rdv uniquement"),
]

SUPPORT_MODE_CHOICES = [
    ("individuel", "Individuel, Personnalisé"),
    ("collectif", "Collectif"),
]

SUPPORT_MODE_MAPPING = SUPPORT_MODE_CHOICES + [
    ("individuel", "Accompagnement individualisé"),
    ("individuel", "Accompagnement personnalisé"),
    ("collectif", "groupe"),
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

SERVICE_NAME_LIST = [
    "Accès à un équipement informatique",
    "Accompagnement aux démarches administratives en ligne",
    "Évaluation de compétences numériques",
    "Acquisition de compétences numériques",
    "Vente de matériel informatique",
    "Stockage numérique sécurisé",
    "Pratiquer des activités récréatives numériques",
]

SERVICE_NAME_MAPPING = list(zip(SERVICE_NAME_LIST, SERVICE_NAME_LIST)) + [
    ("Accès à un équipement informatique", "Accès à Internet en autonomie"),
    (
        "Accompagnement aux démarches administratives en ligne",
        "Etre accompagné dans ses démarches administratives",
    ),
    (
        "Accompagnement aux démarches administratives en ligne",
        "Accompagnements proposés aux démarches en ligne",
    ),
    ("Acquisition de compétences numériques", "Etre initié aux outils numériques"),
    (
        "Acquisition de compétences numériques",
        "Formations compétences de base proposées",
    ),
]

FRANCE_REGION_LIST = [
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

FRANCE_DEPARTEMENT_CHOICES = [
    ("Ain", "Ain (01)"),
    ("Aisne", "Aisne (02)"),
    ("Allier", "Allier (03)"),
    ("Alpes-de-Haute-Provence", "Alpes-de-Haute-Provence (04)"),
    ("Hautes-Alpes", "Hautes-Alpes (05)"),
    ("Alpes-Maritimes", "Alpes-Maritimes (06)"),
    ("Ardèche", "Ardèche (07)"),
    ("Ardennes", "Ardennes (08)"),
    ("Ariège", "Ariège (09)"),
    ("Aube", "Aube (10)"),
    ("Aude", "Aude (11)"),
    ("Aveyron", "Aveyron (12)"),
    ("Bouches-du-Rhône", "Bouches-du-Rhône (13)"),
    ("Calvados", "Calvados (14)"),
    ("Cantal", "Cantal (15)"),
    ("Charente", "Charente (16)"),
    ("Charente-Maritime", "Charente-Maritime (17)"),
    ("Cher", "Cher (18)"),
    ("Corrèze", "Corrèze (19)"),
    ("Corse-du-Sud", "Corse-du-Sud (2A)"),
    ("Haute-Corse", "Haute-Corse (2B)"),
    ("Côte-d'Or", "Côte-d'Or (21)"),
    ("Côtes-d'Armor", "Côtes-d'Armor (22)"),
    ("Creuse", "Creuse (23)"),
    ("Dordogne", "Dordogne (24)"),
    ("Doubs", "Doubs (25)"),
    ("Drôme", "Drôme (26)"),
    ("Eure", "Eure (27)"),
    ("Eure-et-Loir", "Eure-et-Loir (28)"),
    ("Finistère", "Finistère (29)"),
    ("Gard", "Gard (30)"),
    ("Haute-Garonne", "Haute-Garonne (31)"),
    ("Gers", "Gers (32)"),
    ("Gironde", "Gironde (33)"),
    ("Hérault", "Hérault (34)"),
    ("Ille-et-Vilaine", "Ille-et-Vilaine (35)"),
    ("Indre", "Indre (36)"),
    ("Indre-et-Loire", "Indre-et-Loire (37)"),
    ("Isère", "Isère (38)"),
    ("Jura", "Jura (39)"),
    ("Landes", "Landes (40)"),
    ("Loir-et-Cher", "Loir-et-Cher (41)"),
    ("Loire", "Loire (42)"),
    ("Haute-Loire", "Haute-Loire (43)"),
    ("Loire-Atlantique", "Loire-Atlantique (44)"),
    ("Loiret", "Loiret (45)"),
    ("Lot", "Lot (46)"),
    ("Lot-et-Garonne", "Lot-et-Garonne (47)"),
    ("Lozère", "Lozère (48)"),
    ("Maine-et-Loire", "Maine-et-Loire (49)"),
    ("Manche", "Manche (50)"),
    ("Marne", "Marne (51)"),
    ("Haute-Marne", "Haute-Marne (52)"),
    ("Mayenne", "Mayenne (53)"),
    ("Meurthe-et-Moselle", "Meurthe-et-Moselle (54)"),
    ("Meuse", "Meuse (55)"),
    ("Morbihan", "Morbihan (56)"),
    ("Moselle", "Moselle (57)"),
    ("Nièvre", "Nièvre (58)"),
    ("Nord", "Nord (59)"),
    ("Oise", "Oise (60)"),
    ("Orne", "Orne (61)"),
    ("Pas-de-Calais", "Pas-de-Calais (62)"),
    ("Puy-de-Dôme", "Puy-de-Dôme (63)"),
    ("Pyrénées-Atlantiques", "Pyrénées-Atlantiques (64)"),
    ("Hautes-Pyrénées", "Hautes-Pyrénées (65)"),
    ("Pyrénées-Orientales", "Pyrénées-Orientales (66)"),
    ("Bas-Rhin", "Bas-Rhin (67)"),
    ("Haut-Rhin", "Haut-Rhin (68)"),
    ("Rhône", "Rhône (69)"),
    ("Haute-Saône", "Haute-Saône (70)"),
    ("Saône-et-Loire", "Saône-et-Loire (71)"),
    ("Sarthe", "Sarthe (72)"),
    ("Savoie", "Savoie (73)"),
    ("Haute-Savoie", "Haute-Savoie (74)"),
    ("Paris", "Paris (75)"),
    ("Seine-Maritime", "Seine-Maritime (76)"),
    ("Seine-et-Marne", "Seine-et-Marne (77)"),
    ("Yvelines", "Yvelines (78)"),
    ("Deux-Sèvres", "Deux-Sèvres (79)"),
    ("Somme", "Somme (80)"),
    ("Tarn", "Tarn (81)"),
    ("Tarn-et-Garonne", "Tarn-et-Garonne (82)"),
    ("Var", "Var (83)"),
    ("Vaucluse", "Vaucluse (84)"),
    ("Vendée", "Vendée (85)"),
    ("Vienne", "Vienne (86)"),
    ("Haute-Vienne", "Haute-Vienne (87)"),
    ("Vosges", "Vosges (88)"),
    ("Yonne", "Yonne (89)"),
    ("Territoire de Belfort", "Territoire de Belfort (90)"),
    ("Essonne", "Essonne (91)"),
    ("Hauts-de-Seine", "Hauts-de-Seine (92)"),
    ("Seine-Saint-Denis", "Seine-Saint-Denis (93)"),
    ("Val-de-Marne", "Val-de-Marne (94)"),
    ("Val-d'Oise", "Val-d'Oise (95)"),
    ("Guadeloupe", "Guadeloupe (971)"),
    ("Martinique", "Martinique (972)"),
    ("Guyane", "Guyane (973)"),
    ("La Réunion", "La Réunion (974)"),
    ("Mayotte", "Mayotte (976)"),
]
