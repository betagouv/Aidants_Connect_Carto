# Aidants Connect: Carto

Aidants Connect ? voir [ici](https://github.com/betagouv/Aidants_Connect)

L'application Carto centralise et met en valeur l'ensemble des structures d'aide au numérique sur le territoire français.

## Pile technique

- Python 3.7
- Django 3.0
- Django Rest Framework 3.11
- PostgreSQL

## Comment installer la base de données (pour Mac OSX)

Utilisez votre gestionnaire de paquets préféré pour installer la base.
L'exemple qui suit emploie le gestionnaire [Homebrew](https://brew.sh) via la commande `brew`.

Dans un terminal, installez [PostgreSQL](https://www.postgresql.org) :

```sh
brew install postgresql
```

Démarrez le service postgresql :

```sh
brew services start postgresql
```

> Ceci démarre le serveur de la base de données et active sa réexécution au login.

Dans le cas où ce serait votre première utilisation de PostgreSQL, créez une base d'essai à votre nom :

```sh
createdb `whoami`
```

Puis, démarrez l'invite de commande PostgreSQL :

```sh
psql
```

Vous pouvez dès à présent visualiser :
* la liste des bases de données existantes avec cette commande PostgreSQL `\list`
* la liste des roles existants avec `\du`

Ajoutez une base `aidants_connect_carto` appartenant au nouvel utilisateur `aidants_connect_carto_team` en poursuivant dans l'invite de commmande PostgreSQL :

```sql
CREATE USER aidants_connect_carto_team;
CREATE DATABASE aidants_connect_carto OWNER aidants_connect_carto_team;
ALTER USER aidants_connect_carto_team CREATEDB;
```

:tada: La base de donnée `aidants_connect_carto` est installée. Vous pouvez la voir et quitter l'invite de commande avec :

```sql
\list
\q
```

## Installer l'application

Dans votre répertoire de travail, créez et activez un environnement virtuel :

```shell
virtualenv venv
source venv/bin/activate
```

Copiez le code sur votre ordinateur :

```shell
git clone git@github.com:betagouv/Aidants_Connect_Carto.git
```

Installez les dépendances :

```shell
pip install -r requirements.txt
```

Si la commande précédente déclenche le message d'erreur suivant `ld: library not found for -lssl`, essayez :

```shell
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

Dupliquez le fichier `.env.example` à la racine du projet en tant que `.env`

Créez un répertoire `staticfiles` à la racine du projet :

```shell
mkdir staticfiles
```

Appliquez les migrations de la base de données :

```shell
python manage.py migrate
```

Créez un _superuser_ :

```shell
python manage.py createsuperuser --username <insert_admin_name>
```

## Lancer l'application

Pour lancer l'application sur le port `3000` :

```shell
python manage.py runserver 3000
```

## Lancer les tests

```shell
python manage.py test aidants_connect_carto.apps.core
```

## Endpoints

```
Interface utilisateur :
/ (home page)
/lieux (search)
/lieux/<place_id>
/lieux/nouveau
/lieux/<place_id>/modifier
/lieux/<place_id>/services/nouveau
/lieux/<place_id>/services/<service_id>/modifier

Rest Framework (HTML UI or JSON depending on the 'content-type') :
/api
/api/places
/api/places/<place_id>
/api/places/<place_id>/services
/api/places/<place_id>/services/<service_id>
/api/address/search

Swagger (HTML) :
/api/swagger/
```
