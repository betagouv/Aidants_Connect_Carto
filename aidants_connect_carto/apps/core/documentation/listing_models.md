



## data source(aidants_connect_carto.apps.core.models.DataSource)

```
DataSource(id, name, description, type, contact_website_url, logo_url, dataset_name, dataset_url, dataset_local_path, dataset_last_updated, import_config, import_comment, created_at, updated_at)
```

|Name|Fullname|Type|Unique|Null/Blank|Comment|Example|
|---|---|---|---|---|---|---|
|id |ID |serial |True |Blank | | |
|name |Le nom du fournisseur de donnée |varchar(300) | | | | |
|description |Une description |text | |Blank | |Plus de détails sur la source de donnée |
|type |Le type de source |varchar(32) | | | | |
|contact_website_url |L'adresse du site internet de la source de donnée |varchar(300) | |Blank | | |
|logo_url |L'adresse du logo de la source de donnée |varchar(300) | |Blank | | |
|dataset_name |Le nom du jeu de donnée |varchar(300) | | | | |
|dataset_url |L'adresse où l'on peut trouver le jeu de donnée |varchar(300) | |Blank | | |
|dataset_local_path |Le chemin d'accès au jeu de donnée |varchar(300) | | | | |
|dataset_last_updated |La date de dernière mise à jour du jeu de donnée |date | |Both | | |
|import_config |Information et configuration de l'import de la donnée |jsonb | |Both | | |
|import_comment |Informations complémentaires sur l'import de la donnée |text | |Blank | | |
|created_at |La date de création |timestamp with time zone | |Blank | | |
|updated_at |La date de dernière modification |timestamp with time zone | |Blank | | |

Options
```
unique_together : (('name', 'dataset_name'),)
```


## place(aidants_connect_carto.apps.core.models.Place)

```
Place(id, name, supporting_structure_name, description, type, status, legal_entity_type, siret, address_raw, address_housenumber, address_street, address_postcode, address_citycode, address_city, address_departement_code, address_departement_name, address_region_name, latitude, longitude, is_itinerant, itinerant_details, is_online, contact_phone_raw, contact_phone, contact_phone_details, contact_email, contact_website_url, contact_facebook_url, contact_twitter_url, contact_youtube_url, opening_hours_raw, opening_hours_osm_format, opening_hours_details, has_equipment_wifi, has_equipment_computer, has_equipment_scanner, has_equipment_printer, equipment_other, has_accessibility_hi, has_accessibility_mi, has_accessibility_pi, has_accessibility_vi, languages, target_audience_raw, target_audience, support_access_raw, support_access, support_mode_raw, support_mode, is_free, price_details, payment_methods, has_label_fs, logo_url, additional_information, data_source, osm_node_id, created_at, updated_at)
```

|Name|Fullname|Type|Unique|Null/Blank|Comment|Example|
|---|---|---|---|---|---|---|
|id |ID |serial |True |Blank | | |
|name |Le nom du lieu |varchar(300) | | | |BetaGouv |
|supporting_structure_name |Le nom de la structure porteuse du lieu |varchar(300) | |Blank | |Services du Premier Ministre |
|description |Une description du lieu |text | |Blank | |L'incubateur de Services Numériques de l'État |
|type |La typologie du lieu |varchar(32) | | |**UNE SEULE valeur possible**<br>- Administration - Collectivité territoriale<br>- Association<br>- Bibliothèque - Médiathèque<br>- Commune (Ville, CCAS, Centre Culturel...)<br>- Centre social<br>- Département (UTPAS, MDS, MDSI, UTAS...)<br>- Espace Public Numérique (EPN)<br>- Organisme de formations<br>- Intercommunalité (EPCI)<br>- La Poste<br>- Maison de quartier<br>- Maison de Service au Public (MSAP)<br>- Pôle Emploi<br>- Point Information Médiation Multi Services (PIMMS)<br>- Préfecture, Sous-Préfecture<br>- Organisme de sécurité sociale (CAF, CPAM, CARSAT, MSA...)<br>- Tiers-lieu & coworking, FabLab<br>- Autre, Inconnu |Administration |
|status |Le statut du lieu |varchar(32) | | |**UNE SEULE valeur possible**<br>- Public<br>- Privé<br>- Public / Privé<br>- Autre, Inconnu |Public |
|legal_entity_type |La nature juridique du lieu |varchar(32) | | |**UNE SEULE valeur possible**<br>- Association<br>- Collectivité locale ou territoriale<br>- Coopérative d'Activités et d'Entrepreneur·es (CAE)<br>- Établissement public de coopération intercommunale (EPCI)<br>- Établissement public à caractère industriel et commercial (EPIC)<br>- Établissement public à caractère scientifique, culturel et professionnel (EPSCP)<br>- Groupement d'intérêt public (GIP)<br>- Société par actions simplifiée (SAS)<br>- Société à responsabilité limitée (SARL)<br>- Société par actions simplifiée unipersonnelle (SASU)<br>- société coopérative d’intérêt collectif (SCIC)<br>- Société coopérative et participative (SCOP)<br>- Société publique locale (SPL)<br>- Autre, Inconnu | |
|siret |Coordonnées juridiques (SIRET) |varchar(14) | |Blank | | |
|address_raw |L'adresse complète |varchar(300) | | | |20 Avenue de Ségur 75007 Paris |
|address_housenumber |Le numéro avec indice de répétition éventuel (bis, ter, A, B) |varchar(15) | |Blank | |20 |
|address_street |Le nom de la rue |varchar(150) | |Blank | |Avenue de Ségur |
|address_postcode |Le code postal |varchar(5) | |Blank | |75007 |
|address_citycode |Le code INSEE de la commune |varchar(5) | |Blank | |75107 |
|address_city |Le nom de la commune |varchar(150) | |Blank | |Paris |
|address_departement_code |Le numéro de département |varchar(3) | |Blank | |75 |
|address_departement_name |Le nom du département |varchar(150) | |Blank |**UNE SEULE valeur possible**<br>- Ain (01)<br>- Aisne (02)<br>- Allier (03)<br>- Alpes-de-Haute-Provence (04)<br>- Hautes-Alpes (05)<br>- Alpes-Maritimes (06)<br>- Ardèche (07)<br>- Ardennes (08)<br>- Ariège (09)<br>- Aube (10)<br>- Aude (11)<br>- Aveyron (12)<br>- Bouches-du-Rhône (13)<br>- Calvados (14)<br>- Cantal (15)<br>- Charente (16)<br>- Charente-Maritime (17)<br>- Cher (18)<br>- Corrèze (19)<br>- Corse-du-Sud (2A)<br>- Haute-Corse (2B)<br>- Côte-d'Or (21)<br>- Côtes-d'Armor (22)<br>- Creuse (23)<br>- Dordogne (24)<br>- Doubs (25)<br>- Drôme (26)<br>- Eure (27)<br>- Eure-et-Loir (28)<br>- Finistère (29)<br>- Gard (30)<br>- Haute-Garonne (31)<br>- Gers (32)<br>- Gironde (33)<br>- Hérault (34)<br>- Ille-et-Vilaine (35)<br>- Indre (36)<br>- Indre-et-Loire (37)<br>- Isère (38)<br>- Jura (39)<br>- Landes (40)<br>- Loir-et-Cher (41)<br>- Loire (42)<br>- Haute-Loire (43)<br>- Loire-Atlantique (44)<br>- Loiret (45)<br>- Lot (46)<br>- Lot-et-Garonne (47)<br>- Lozère (48)<br>- Maine-et-Loire (49)<br>- Manche (50)<br>- Marne (51)<br>- Haute-Marne (52)<br>- Mayenne (53)<br>- Meurthe-et-Moselle (54)<br>- Meuse (55)<br>- Morbihan (56)<br>- Moselle (57)<br>- Nièvre (58)<br>- Nord (59)<br>- Oise (60)<br>- Orne (61)<br>- Pas-de-Calais (62)<br>- Puy-de-Dôme (63)<br>- Pyrénées-Atlantiques (64)<br>- Hautes-Pyrénées (65)<br>- Pyrénées-Orientales (66)<br>- Bas-Rhin (67)<br>- Haut-Rhin (68)<br>- Rhône (69)<br>- Haute-Saône (70)<br>- Saône-et-Loire (71)<br>- Sarthe (72)<br>- Savoie (73)<br>- Haute-Savoie (74)<br>- Paris (75)<br>- Seine-Maritime (76)<br>- Seine-et-Marne (77)<br>- Yvelines (78)<br>- Deux-Sèvres (79)<br>- Somme (80)<br>- Tarn (81)<br>- Tarn-et-Garonne (82)<br>- Var (83)<br>- Vaucluse (84)<br>- Vendée (85)<br>- Vienne (86)<br>- Haute-Vienne (87)<br>- Vosges (88)<br>- Yonne (89)<br>- Territoire de Belfort (90)<br>- Essonne (91)<br>- Hauts-de-Seine (92)<br>- Seine-Saint-Denis (93)<br>- Val-de-Marne (94)<br>- Val-d'Oise (95)<br>- Guadeloupe (971)<br>- Martinique (972)<br>- Guyane (973)<br>- La Réunion (974)<br>- Mayotte (976) |Paris |
|address_region_name |Le nom de la région |varchar(150) | |Blank |**UNE SEULE valeur possible**<br>- Auvergne-Rhône-Alpes<br>- Bourgogne-Franche-Comté<br>- Bretagne<br>- Centre-Val de Loire<br>- Corse<br>- Grand Est<br>- Hauts-de-France<br>- Île-de-France<br>- Normandie<br>- Nouvelle-Aquitaine<br>- Occitanie<br>- Pays de la Loire<br>- Provence-Alpes-Côte d'Azur<br>- Guadeloupe<br>- Martinique<br>- Guyane<br>- La Réunion<br>- Mayotte |Île-de-France |
|latitude |La latitude (coordonnée géographique) |double precision | |Both | |48.850699 |
|longitude |La longitude (coordonnée géographique) |double precision | |Both | |2.308628 |
|is_itinerant |Le lieu est-il itinérant ? |boolean | | | | |
|itinerant_details |Le details des déplacements |text | |Blank | | |
|is_online |Le lieu est-il uniquement en ligne ? |boolean | | | | |
|contact_phone_raw |Le numéro de téléphone brut |varchar(300) | | | | |
|contact_phone |Le numéro de téléphone |varchar(10) | |Both | |0123456789 |
|contact_phone_details |Le details du numéro de téléphone (horaires, prix, ...) |text | |Blank | | |
|contact_email |Le courriel |varchar(150) | |Blank | |exemple@email.fr |
|contact_website_url |L'adresse du site internet |varchar(300) | |Blank | |https://beta.gouv.fr/ |
|contact_facebook_url |L'adresse de la page Facebook |varchar(300) | |Blank | | |
|contact_twitter_url |L'adresse de la page Twitter |varchar(300) | |Blank | |https://twitter.com/betagouv |
|contact_youtube_url |L'adresse de la page Youtube |varchar(300) | |Blank | | |
|opening_hours_raw |Les horaires d'ouverture brut |text | |Blank | |Du lundi au vendredi de 8h à 20h |
|opening_hours_osm_format |Les horaires d'ouverture au format OpenStreetMap |varchar(150) | |Blank | |Mo-Fr 8:00-20:00 |
|opening_hours_details |Des détails supplémentaires sur les horaires d'ouverture |text | |Blank | |sur rendez-vous le Mardi, porte-ouvertes le Mercredi, ... |
|has_equipment_wifi |WiFi |boolean | | | | |
|has_equipment_computer |Ordinateur |boolean | | | | |
|has_equipment_scanner |Scanner |boolean | | | | |
|has_equipment_printer |Imprimante |boolean | | | | |
|equipment_other |Autres équipements disponibles |varchar(300) | |Blank | | |
|has_accessibility_hi |Handicap auditif |boolean | | | | |
|has_accessibility_mi |Handicap moteur |boolean | | | | |
|has_accessibility_pi |Handicap intellectuel ou psychique |boolean | | | | |
|has_accessibility_vi |Handicap visuel |boolean | | | | |
|languages |Langues parlées |varchar(150) | |Blank | |Français, Anglais, ... |
|target_audience_raw |Public(s) cible brut |text | |Blank | | |
|target_audience |Public(s) cible |varchar(32)[] | |Blank |**PLUSIEURS valeurs possible**<br>- Tout public<br>- Allocataires<br>- Demandeurs d'emploi<br>- Étrangers<br>- Familles<br>- -25 ans, Jeunes<br>- Personnes en situation de handicap<br>- Séniors | |
|support_access_raw |Modalité(s) d'accès brut |text | |Blank | | |
|support_access |Modalité(s) d'accès |varchar(32)[] | |Blank |**PLUSIEURS valeurs possible**<br>- Accès libre<br>- Sur inscription ou rendez-vous<br>- Public cible uniquement<br>- Adhérents uniquement |libre, inscription, adhérent, ... |
|support_mode_raw |Modalité(s) d'accompagnement brut |text | |Blank | | |
|support_mode |Modalité(s) d'accompagnement |varchar(32)[] | |Blank |**PLUSIEURS valeurs possible**<br>- Individuel, Personnalisé<br>- Collectif |individuel, collectif, ... |
|is_free |Le lieu est-il gratuit ? |boolean | | | | |
|price_details |Le details des prix du lieu |text | |Blank | | |
|payment_methods |Les moyens de paiement |varchar(150) | |Blank | |Espèces, Carte Bancaire, ... |
|has_label_fs |Labellisé France Service |boolean | | | | |
|logo_url |L'adresse du logo du lieu |varchar(300) | |Blank | |https://beta.gouv.fr/img/logo_twitter_image-2019.jpg |
|additional_information |Informations additionnelles stockées au format JSON |jsonb | |Both | | |
|data_source |data source |integer | |Null |FK:aidants_connect_carto.apps.core.models.DataSource | |
|osm_node_id |OpenStreetMap node id |integer | |Both | |5266052428 |
|created_at |La date de création |timestamp with time zone | |Blank | | |
|updated_at |La date de dernière modification |timestamp with time zone | |Blank | | |

Options
```
ordering : ['id']
```


## service(aidants_connect_carto.apps.core.models.Service)

```
Service(id, name, description, siret, target_audience, support_access, support_mode, schedule_hours_raw, schedule_hours_osm_format, is_free, price_details, payment_methods, has_label_aidants_connect, label_other, additional_information, place, created_at, updated_at)
```

|Name|Fullname|Type|Unique|Null/Blank|Comment|Example|
|---|---|---|---|---|---|---|
|id |ID |serial |True |Blank | | |
|name |Le nom du service |varchar(300) | | | | |
|description |Une description du service |text | |Blank | | |
|siret |Coordonnées juridiques (SIRET) |varchar(14) | |Blank | | |
|target_audience |Public cible (s'il est différent du public cible du lieu) |varchar(32)[] | |Blank |**PLUSIEURS valeurs possible**<br>- Tout public<br>- Allocataires<br>- Demandeurs d'emploi<br>- Étrangers<br>- Familles<br>- -25 ans, Jeunes<br>- Personnes en situation de handicap<br>- Séniors | |
|support_access |Modalités d'accès (si différent du lieu) |varchar(32) | |Blank |**UNE SEULE valeur possible**<br>- Accès libre<br>- Sur inscription ou rendez-vous<br>- Public cible uniquement<br>- Adhérents uniquement |libre, inscription, adhérent, ... |
|support_mode |Modalités d'accompagnement (si différent du lieu) |varchar(32) | |Blank |**UNE SEULE valeur possible**<br>- Individuel, Personnalisé<br>- Collectif |individuel, collectif, ... |
|schedule_hours_raw |Les horaires du service (s'ils sont différents des horaires du lieu) |text | |Blank | |Le mardi de 14h à 18h |
|schedule_hours_osm_format |Les horaires du service au format OpenStreetMap |varchar(150) | |Blank | |Tu 14:00-18:00 |
|is_free |Le service est-il gratuit ? |boolean | | | | |
|price_details |Le details des prix du service |text | |Blank | | |
|payment_methods |Les moyens de paiements spécifiques à ce service |text | |Blank | | |
|has_label_aidants_connect |Labellisé Aidants Connect |boolean | | | | |
|label_other |Autres labels |varchar(300) | |Blank | | |
|additional_information |Informations additionnelles stockées au format JSON |jsonb | |Both | | |
|place |place |integer | | |FK:aidants_connect_carto.apps.core.models.Place | |
|created_at |La date de création |timestamp with time zone | |Blank | | |
|updated_at |La date de dernière modification |timestamp with time zone | |Blank | | |

Options
```
ordering : ['id']
```
