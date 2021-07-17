#!/bin/bash
# shellcheck disable=SC2034
BACKUP_PS1=PS1
PS1=""
export PS1

clear

# installing python requirements
python -m pip install Django
python -m pip install django-mptt
# install Pillow for images
python -m pip install Pillow
# rest framework
python -m pip install djangorestframework
python -m pip install markdown
python -m pip install djangorestframework

clear

# migrate
python manage.py makemigrations
python manage.py migrate
clear

# remove setup
rm setup.bat
rm setup.sh

PS1=BACKUP_PS1
export PS1
