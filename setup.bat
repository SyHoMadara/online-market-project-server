@echo off






python manage.py makemigrations
python manage.py migrate


del /f setup.sh
del /f setup.bat



