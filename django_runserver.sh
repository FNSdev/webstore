#!/bin/bash

path=$1
if [ -d $path ] & [ -e "$path/manage.py" ]
then
    cd $path
    cd ..
    source venv/bin/activate
    cd $path
    python manage.py runserver
else
    echo 'Wrong directory'
fi
