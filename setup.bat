@echo off
cls


python -m pip install Django
python -m install django-mptt

python -m pip install Pillow

python -m pip install djangorestframework
python -m pip install markdown
python -m pip install djangorestframework

cls


python manage.py makemigrations
python manage.py migrate
cls

del /f setup.sh
del /f setup.bat

@echo on
