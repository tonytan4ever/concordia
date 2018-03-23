echo Running migrations
./manage.py migrate

echo Running collectstatic
./manage.py collectstatic --clear --noinput -v0

echo Running Django dev server in background
./manage.py runserver 0:80

echo Running celery 
# celery -A concordia worker -l info


# echo running gunicorn
# gunicorn -c gunicorn.conf concordia.wsgi:application

