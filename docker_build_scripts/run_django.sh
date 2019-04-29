sh /install_dependencies.sh

source production-env

cd /football_stats
python manage.py makemigrations
python manage.py migrate
python manage.py shell < create_superuser.py
python manage.py shell < insert_initial_data.py
python manage.py collectstatic --no-input

gunicorn --bind=0.0.0.0:8000 --workers=3 football_stats.wsgi:application &
python manage.py process_tasks