#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

python manage.py shell -c "
from django.contrib.auth.models import User;
if not User.objects.filter(username='${DJANGO_SUPERUSER_USER}').exists():
    User.objects.create_superuser(
        '${DJANGO_SUPERUSER_USER}',
        '${DJANGO_SUPERUSER_EMAIL}',
        '${DJANGO_SUPERUSER_PASSWORD}'
    )"

exec "$@"