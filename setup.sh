#!/bin/bash
export PS1=""
clear

# installing python requirements

clear

# migrate
python manage.py makemigrations
python manage.py migrate
clear

# remove setup
rm setup.cmd
rm setup.sh
