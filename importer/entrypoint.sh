mkdir -p /app/logs
touch /app/logs/importer.log

#cd importer

echo Running django server
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000 &

sleep 10

echo Running celery worker
celery -A importer worker -l info -c 10

