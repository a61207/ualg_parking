tar -xf ualgParking\settings.zip -C ualgParking
pip3 install -r requirements.txt
python manage.py makemigrations main
python manage.py migrate
python manage.py loaddata popdb.json

pause