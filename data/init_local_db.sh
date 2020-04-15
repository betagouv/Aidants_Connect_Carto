####################
## VARIABLES
####################

database_name="aidants_connect_carto"
database_user="aidants_connect_carto_team"
admin_email="admin@email.com"
staff_email="staff@email.com"

database_already_exists=false
database_do_backup=false


####################
# FUNCTIONS: create_superuser, create_staff_user
####################

create_superuser() {
echo "Superuser: create" $admin_email

python manage.py createsuperuser --username $admin_email --email $admin_email

echo "Superuser: done"
}


create_staff_user() {
echo "Staff User: create"

python manage.py shell << END
from aidants_connect_web.models import Aidant
staff = Aidant.objects.create(username='staff@email.com',
    email='staff@email.com', is_staff=True)
staff.set_password('staff')
staff.save()
END

echo "Staff User: done"
}


####################
# SCRIPT
####################

echo "Database: checking that it doesn't already exist"

if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='$database_name'" )" = '1' ] ; then
    echo "Database already exists !"
    database_already_exists=true
else
    echo "Database does not exist"
fi

if $database_already_exists ; then
    echo "Database: do you want to make a backup first ? (y/n)"
    read answer
    if [ "$answer" != "${answer#[Yy]}" ] ;then
        echo "Database: will be backed up to db.json"
        database_do_backup=true
        python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
        echo "Database: successfully backed up to db.json"
    fi
fi

echo "Database: setting up"

psql -c "DROP DATABASE $database_name"
psql -c "CREATE DATABASE $database_name OWNER $database_user"
psql -c "ALTER USER $database_user CREATEDB"

echo "Database: migrations"

python manage.py migrate

if $database_do_backup ; then
    echo "Database: loading data from db.json"
    python manage.py loaddata db.json
else
    create_superuser
fi

echo "You're done"
echo "To start the server: 'python manage.py runserver 3000'"