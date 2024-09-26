find . -name "*.pyc" -exec rm -f {} \;
rm  static/immobili/*
rm db.sqlite3
rm */migrations/00*
python3 manage.py makemigrations && python manage.py migrate

DJANGO_SUPERUSER_USERNAME="simone" \
DJANGO_SUPERUSER_PASSWORD="paperinik88" \
DJANGO_SUPERUSER_EMAIL="note@type.io" \
python3 manage.py createsuperuser --noinput

#python3 manage.py runserver 8081 &

#sleep 5

#curl http://127.0.0.1:8081/init_db/
