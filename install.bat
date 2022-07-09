python -m venv venv | .\venv\Scripts\activate | tar -xf ualgParking\settings.zip -C ualgParking | pip3 install -r requirements.txt | python manage.py migrate |python manage.py loaddata inidb.json

pause