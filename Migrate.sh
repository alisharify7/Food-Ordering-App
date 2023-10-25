#! /usr/bin/bash

# sudo chmod +x ./MakeMigrate

# if migrations directory exists delete it and init
#      migrations again

if [[ "$1" == "\\" && "$2" == "migrations" ]]; then
    echo "Migrations directory already exists."
    rm -rf "migrations"
    echo "deleting Migrations directory"
else
    flask db init && flask db migrate && flask db upgrade
fi