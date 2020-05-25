# Documentation

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Modèle de donnée](#mod%C3%A8le-de-donn%C3%A9e)
  - [Où trouver le modèle de donnée ?](#o%C3%B9-trouver-le-mod%C3%A8le-de-donn%C3%A9e-)
  - [Générer la documentation du modèle de donnée en Markdown](#g%C3%A9n%C3%A9rer-la-documentation-du-mod%C3%A8le-de-donn%C3%A9e-en-markdown)
    - [Package](#package)
    - [Commande](#commande)
    - [Améliorations](#am%C3%A9liorations)
  - [Générer la documentation du modèle de donnée en graph (png)](#g%C3%A9n%C3%A9rer-la-documentation-du-mod%C3%A8le-de-donn%C3%A9e-en-graph-png)
    - [Package](#package-1)
    - [Commande](#commande-1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Modèle de donnée

### Où trouver le modèle de donnée ?

- en code Python: [core/models.py](https://github.com/betagouv/Aidants_Connect_Carto/blob/master/aidants_connect_carto/apps/core/listing_models.py)
- en texte (Markdown): [core/documentation/listing_models.md](https://github.com/betagouv/Aidants_Connect_Carto/blob/master/aidants_connect_carto/apps/core/documentation/models.md)
- en image (PNG): [core/documentation/graph_models_with_fields.png](https://github.com/betagouv/Aidants_Connect_Carto/blob/master/aidants_connect_carto/apps/core/documentation/graph_models_with_fields.png) & [core/documentation/graph_models_without_fields.png](https://github.com/betagouv/Aidants_Connect_Carto/blob/master/aidants_connect_carto/apps/core/documentation/graph_models_without_fields.png)

### Générer la documentation du modèle de donnée en Markdown

#### Package

[django-modelsdoc](https://github.com/tell-k/django-modelsdoc)

#### Commande

```
python manage.py listing_models --app core --format md --output aidants_connect_carto/apps/core/documentation/listing_models.md
```

#### Améliorations

Pouvoir Afficher un choice par ligne:
- https://github.com/tell-k/django-modelsdoc/issues/8
- `MODELSDOC_FIELD_WRAPPER = 'aidants_connect_carto.apps.core.documentation.custom_field_wrapper'`

### Générer la documentation du modèle de donnée en graph (png)

#### Package

[django-extensions: graph_models](https://django-extensions.readthedocs.io/en/latest/graph_models.html)

#### Commande

```
// avec les champs
python manage.py graph_models -a -I DataSource,Place,Service --verbose-names --disable-sort-fields --hide-edge-labels --arrow-shape normal -o aidants_connect_carto/apps/core/documentation/graph_models_with_fields.png

// sans les champs
python manage.py graph_models -a -I DataSource,Place,Service --verbose-names --disable-fields --hide-edge-labels --arrow-shape normal -o aidants_connect_carto/apps/core/documentation/graph_models_without_fields.png
```
