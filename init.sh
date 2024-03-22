echo "Initialize Data Base..."
python manage.py makemigrations && python manage.py migrate

echo "Create Super User:"
python manage.py createsuperuser