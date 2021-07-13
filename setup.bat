@echo off
cls


cls


python manage.py makemigrations
python manage.py migrate
cls

del /f setup.sh
del /f setup.bat



