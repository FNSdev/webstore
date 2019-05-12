#!/bin/bash

path=$1
if [ -d $path ] & [ -e "$path/manage.py" ]
then
    cd $path
    cd ..
    source venv/bin/activate
    cd $path
    export DJANGO_SETTINGS_MODULE=config.local_settings
    python manage.py runserver
else
    echo 'Wrong directory'
fi
