# schema.json

## Documentation

Doc Etalab : https://guides.etalab.gouv.fr/producteurs-schemas/

Table Schema : https://specs.frictionlessdata.io/table-schema/

## Outils de création

Template de repo pour se lancer dans la création de schémas : https://github.com/etalab/tableschema-template/

## Outils de validation

- Validata : https://go.validata.fr/
- Goodtables : http://docs.goodtables.io/index.html
- Frictionless : https://pypi.org/project/frictionless/

Etalab csv-gg (create forms from Table Schemas and let users create valid CSV rows) : https://github.com/etalab/csv-gg / https://csv-gg.etalab.studio/

### Frictionless (Python package)

```
frictionless validate --source-type schema data/schema/schema.json
frictionless validate --schema data/schema/schema.json data/schema/exemple-valide.csv
```

## Exemples

https://github.com/etalab/schema.data.gouv.fr/

https://git.opendatafrance.net/scdl/marches-publics/-/blob/master/schema.json

## Lieux de l'inclusion numérique

### choix multiples

```
with space after comma
(?:(?:^|, )(Dog|Cat|Bird|Mouse))+$
- "Dog, Cat"

without space after comma --> https://regexr.com/5djcs
(?:(?:^|,)(Dog|Cat|Bird|Mouse))+$
- "Dog,Cat"

without space after comma and allow empty
(?:(?:^|,)(|Dog|Cat|Bird|Mouse))+$
- "Dog,Cat,"
```

### adresse

### horaires

### last_updated

TODO

### primaryKey

```
"primaryKey": "id"
```

### source

Spécifier la source de donnée du lieu
