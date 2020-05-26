



## data source(aidants_connect_carto.apps.core.models.DataSource)

```
DataSource(id, name, description, type, contact_website_url, logo_url, dataset_name, dataset_url, dataset_local_path, dataset_last_updated, import_config, import_comment, created_at, updated_at)
```

|Name|Fullname|Type|Unique|Null/Blank|Comment|
|---|---|---|---|---|---|
|id |ID |serial |True |Blank | |
|name |Le nom du fournisseur de donnée |varchar(300) | | | |
|description |Une description |text | |Blank | |
|type |Le type de source |varchar(32) | | | |
|contact_website_url |L'adresse du site internet de la source de donnée |varchar(300) | |Blank | |
|logo_url |L'adresse du logo de la source de donnée |varchar(300) | |Blank | |
|dataset_name |Le nom du jeu de donnée |varchar(300) | | | |
|dataset_url |L'adresse où l'on peut trouver le jeu de donnée |varchar(300) | |Blank | |
|dataset_local_path |Le chemin d'accès au jeu de donnée |varchar(300) | | | |
|dataset_last_updated |La date de dernière mise à jour du jeu de donnée |date | |Both | |
|import_config |Information et configuration de l'import de la donnée |jsonb | |Both | |
|import_comment |Informations complémentaires sur l'import de la donnée |text | |Blank | |
|created_at |La date de création |timestamp with time zone | |Blank | |
|updated_at |La date de dernière modification |timestamp with time zone | |Blank | |


## place(aidants_connect_carto.apps.core.models.Place)

```
Place(id, name, supporting_structure_name, description, type, status, legal_entity_type, siret, address_raw, address_housenumber, address_street, address_postcode, address_citycode, address_city, address_departement_code, address_departement_name, address_region_name, latitude, longitude, is_itinerant, itinerant_details, is_online, contact_phone_raw, contact_phone, contact_phone_details, contact_email, contact_website_url, contact_facebook_url, contact_twitter_url, contact_youtube_url, opening_hours_raw, opening_hours_osm_format, has_equipment_wifi, has_equipment_computer, has_equipment_scanner, has_equipment_printer, equipment_other, has_accessibility_hi, has_accessibility_mi, has_accessibility_pi, has_accessibility_vi, languages, target_audience_raw, target_audience, payment_methods, has_label_fs, logo_url, additional_information, data_source, osm_node_id, created_at, updated_at)
```

|Name|Fullname|Type|Unique|Null/Blank|Comment|
|---|---|---|---|---|---|
|id |ID |serial |True |Blank | |
|name |Le nom du lieu |varchar(300) | | | |
|supporting_structure_name |Le nom de la structure porteuse du lieu |varchar(300) | |Blank | |
|description |Une description du lieu |text | |Blank | |
|type |La typologie du lieu |varchar(32) | | |centre social:Centre social, securite sociale:Organisme de sécurité sociale (CAF, CPAM, CARSAT, MSA...), tiers lieu:Tiers-lieu & coworking, FabLab, association:Association, maison quartier:Maison de quartier, pimms:Point Information Médiation Multi Services (PIMMS), msap:Maison de Service au Public (MSAP), bibliotheque:Bibliothèque - Médiathèque, formation:Organisme de formations, pole emploi:Pôle Emploi, commune:Commune (Ville, CCAS, Centre Culturel...), intercommunalite:Intercommunalité (EPCI), administration:Administration - Collectivité territoriale, departement:Département (UTPAS, MDS, MDSI, UTAS...), prefecture:Préfecture, Sous-Préfecture, autre:Autre, Inconnu |
|status |Le statut du lieu |varchar(32) | | |public:Public, prive:Privé, public-prive:Public / Privé, autre:Autre, Inconnu |
|legal_entity_type |La nature juridique du lieu |varchar(32) | | |association:Association, collectivite:Collectivité locale ou territoriale, cae:Coopérative d'Activités et d'Entrepreneur·es (CAE), epci:Établissement public de coopération intercommunale (EPCI), epic:Établissement public à caractère industriel et commercial (EPIC), epscp:Établissement public à caractère scientifique, culturel et professionnel (EPSCP), gip:Groupement d'intérêt public (GIP), sas:Société par actions simplifiée (SAS), sarl:Société à responsabilité limitée (SARL), sasu:Société par actions simplifiée unipersonnelle (SASU), scic:société coopérative d’intérêt collectif (SCIC), scop:Société coopérative et participative (SCOP), spl:Société publique locale (SPL), autre:Autre, Inconnu |
|siret |Coordonnées juridiques (SIRET) |varchar(14) | |Blank | |
|address_raw |L'adresse complète |varchar(300) | | | |
|address_housenumber |Le numéro avec indice de répétition éventuel (bis, ter, A, B) |varchar(15) | |Blank | |
|address_street |Le nom de la rue |varchar(150) | |Blank | |
|address_postcode |Le code postal |varchar(5) | |Blank | |
|address_citycode |Le code INSEE de la commune |varchar(5) | |Blank | |
|address_city |Le nom de la commune |varchar(150) | |Blank | |
|address_departement_code |Le numéro de département |varchar(3) | |Blank | |
|address_departement_name |Le nom du département |varchar(150) | |Blank |Ain:Ain (01), Aisne:Aisne (02), Allier:Allier (03), Alpes-de-Haute-Provence:Alpes-de-Haute-Provence (04), Hautes-Alpes:Hautes-Alpes (05), Alpes-Maritimes:Alpes-Maritimes (06), Ardèche:Ardèche (07), Ardennes:Ardennes (08), Ariège:Ariège (09), Aube:Aube (10), Aude:Aude (11), Aveyron:Aveyron (12), Bouches-du-Rhône:Bouches-du-Rhône (13), Calvados:Calvados (14), Cantal:Cantal (15), Charente:Charente (16), Charente-Maritime:Charente-Maritime (17), Cher:Cher (18), Corrèze:Corrèze (19), Corse-du-Sud:Corse-du-Sud (2A), Haute-Corse:Haute-Corse (2B), Côte-d'Or:Côte-d'Or (21), Côtes-d'Armor:Côtes-d'Armor (22), Creuse:Creuse (23), Dordogne:Dordogne (24), Doubs:Doubs (25), Drôme:Drôme (26), Eure:Eure (27), Eure-et-Loir:Eure-et-Loir (28), Finistère:Finistère (29), Gard:Gard (30), Haute-Garonne:Haute-Garonne (31), Gers:Gers (32), Gironde:Gironde (33), Hérault:Hérault (34), Ille-et-Vilaine:Ille-et-Vilaine (35), Indre:Indre (36), Indre-et-Loire:Indre-et-Loire (37), Isère:Isère (38), Jura:Jura (39), Landes:Landes (40), Loir-et-Cher:Loir-et-Cher (41), Loire:Loire (42), Haute-Loire:Haute-Loire (43), Loire-Atlantique:Loire-Atlantique (44), Loiret:Loiret (45), Lot:Lot (46), Lot-et-Garonne:Lot-et-Garonne (47), Lozère:Lozère (48), Maine-et-Loire:Maine-et-Loire (49), Manche:Manche (50), Marne:Marne (51), Haute-Marne:Haute-Marne (52), Mayenne:Mayenne (53), Meurthe-et-Moselle:Meurthe-et-Moselle (54), Meuse:Meuse (55), Morbihan:Morbihan (56), Moselle:Moselle (57), Nièvre:Nièvre (58), Nord:Nord (59), Oise:Oise (60), Orne:Orne (61), Pas-de-Calais:Pas-de-Calais (62), Puy-de-Dôme:Puy-de-Dôme (63), Pyrénées-Atlantiques:Pyrénées-Atlantiques (64), Hautes-Pyrénées:Hautes-Pyrénées (65), Pyrénées-Orientales:Pyrénées-Orientales (66), Bas-Rhin:Bas-Rhin (67), Haut-Rhin:Haut-Rhin (68), Rhône:Rhône (69), Haute-Saône:Haute-Saône (70), Saône-et-Loire:Saône-et-Loire (71), Sarthe:Sarthe (72), Savoie:Savoie (73), Haute-Savoie:Haute-Savoie (74), Paris:Paris (75), Seine-Maritime:Seine-Maritime (76), Seine-et-Marne:Seine-et-Marne (77), Yvelines:Yvelines (78), Deux-Sèvres:Deux-Sèvres (79), Somme:Somme (80), Tarn:Tarn (81), Tarn-et-Garonne:Tarn-et-Garonne (82), Var:Var (83), Vaucluse:Vaucluse (84), Vendée:Vendée (85), Vienne:Vienne (86), Haute-Vienne:Haute-Vienne (87), Vosges:Vosges (88), Yonne:Yonne (89), Territoire de Belfort:Territoire de Belfort (90), Essonne:Essonne (91), Hauts-de-Seine:Hauts-de-Seine (92), Seine-Saint-Denis:Seine-Saint-Denis (93), Val-de-Marne:Val-de-Marne (94), Val-d'Oise:Val-d'Oise (95), Guadeloupe:Guadeloupe (971), Martinique:Martinique (972), Guyane:Guyane (973), La Réunion:La Réunion (974), Mayotte:Mayotte (976) |
|address_region_name |Le nom de la région |varchar(150) | |Blank |Auvergne-Rhône-Alpes:Auvergne-Rhône-Alpes, Bourgogne-Franche-Comté:Bourgogne-Franche-Comté, Bretagne:Bretagne, Centre-Val de Loire:Centre-Val de Loire, Corse:Corse, Grand Est:Grand Est, Hauts-de-France:Hauts-de-France, Île-de-France:Île-de-France, Normandie:Normandie, Nouvelle-Aquitaine:Nouvelle-Aquitaine, Occitanie:Occitanie, Pays de la Loire:Pays de la Loire, Provence-Alpes-Côte d'Azur:Provence-Alpes-Côte d'Azur, Guadeloupe:Guadeloupe, Martinique:Martinique, Guyane:Guyane, La Réunion:La Réunion, Mayotte:Mayotte |
|latitude |La latitude (coordonnée géographique) |double precision | |Both | |
|longitude |La longitude (coordonnée géographique) |double precision | |Both | |
|is_itinerant |Le lieu est-il itinérant ? |boolean | | | |
|itinerant_details |Le details des déplacements |text | |Blank | |
|is_online |Le lieu est-il uniquement en ligne ? |boolean | | | |
|contact_phone_raw |Le numéro de téléphone brut |varchar(300) | | | |
|contact_phone |Le numéro de téléphone |varchar(10) | |Both | |
|contact_phone_details |Le details du numéro de téléphone (horaires, prix, ...) |text | |Blank | |
|contact_email |Le courriel |varchar(150) | |Blank | |
|contact_website_url |L'adresse du site internet |varchar(300) | |Blank | |
|contact_facebook_url |L'adresse de la page Facebook |varchar(300) | |Blank | |
|contact_twitter_url |L'adresse de la page Twitter |varchar(300) | |Blank | |
|contact_youtube_url |L'adresse de la page Youtube |varchar(300) | |Blank | |
|opening_hours_raw |Les horaires d'ouverture |text | |Blank | |
|opening_hours_osm_format |Les horaires d'ouverture au format OpenStreetMap |varchar(150) | |Blank | |
|has_equipment_wifi |WiFi |boolean | | | |
|has_equipment_computer |Ordinateur |boolean | | | |
|has_equipment_scanner |Scanner |boolean | | | |
|has_equipment_printer |Imprimante |boolean | | | |
|equipment_other |Autres équipements disponibles |varchar(300) | |Blank | |
|has_accessibility_hi |Handicap auditif |boolean | | | |
|has_accessibility_mi |Handicap moteur |boolean | | | |
|has_accessibility_pi |Handicap intellectuel ou psychique |boolean | | | |
|has_accessibility_vi |Handicap visuel |boolean | | | |
|languages |Langues parlées |varchar(150) | |Blank | |
|target_audience_raw |Le public cible |text | |Blank | |
|target_audience |Public cible |varchar(32)[] | |Blank | |
|payment_methods |Les moyens de paiement |varchar(150) | |Blank | |
|has_label_fs |Labellisé France Service |boolean | | | |
|logo_url |L'adresse du logo du lieu |varchar(300) | |Blank | |
|additional_information |Informations additionnelles stockées au format JSON |jsonb | |Both | |
|data_source |data source |integer | |Null |FK:aidants_connect_carto.apps.core.models.DataSource |
|osm_node_id |OpenStreetMap node id |integer | |Both | |
|created_at |La date de création |timestamp with time zone | |Blank | |
|updated_at |La date de dernière modification |timestamp with time zone | |Blank | |

Options
```
ordering : ['id']
```


## service(aidants_connect_carto.apps.core.models.Service)

```
Service(id, name, description, siret, target_audience, support_access, support_mode, schedule_hours_raw, schedule_hours_osm_format, is_free, price_details, payment_methods, has_label_aidants_connect, label_other, additional_information, place, created_at, updated_at)
```

|Name|Fullname|Type|Unique|Null/Blank|Comment|
|---|---|---|---|---|---|
|id |ID |serial |True |Blank | |
|name |Le nom du service |varchar(300) | | | |
|description |Une description du service |text | |Blank | |
|siret |Coordonnées juridiques (SIRET) |varchar(14) | |Blank | |
|target_audience |Public cible (s'il est différent du public cible du lieu) |varchar(32)[] | |Blank | |
|support_access |Modalités d'accès |varchar(32) | |Blank |libre:Accès libre, inscription:Sur inscription ou rendez-vous, public cible:Public cible uniquement, adherents:Adhérents uniquement |
|support_mode |Modalités d'accompagnement |varchar(32) | |Blank |individuel:Individuel, Personnalisé, collectif:Collectif |
|schedule_hours_raw |Les horaires du service (s'ils sont différents des horaires du lieu) |text | |Blank | |
|schedule_hours_osm_format |Les horaires du service au format OpenStreetMap |varchar(150) | |Blank | |
|is_free |Le service est-il gratuit ? |boolean | | | |
|price_details |Le details des prix |text | |Blank | |
|payment_methods |Les moyens de paiements spécifiques à ce service |text | |Blank | |
|has_label_aidants_connect |Labellisé Aidants Connect |boolean | | | |
|label_other |Autres labels |varchar(300) | |Blank | |
|additional_information |Informations additionnelles stockées au format JSON |jsonb | |Both | |
|place |place |integer | | |FK:aidants_connect_carto.apps.core.models.Place |
|created_at |La date de création |timestamp with time zone | |Blank | |
|updated_at |La date de dernière modification |timestamp with time zone | |Blank | |

Options
```
ordering : ['id']
```



