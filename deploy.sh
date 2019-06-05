#!/bin/bash
set -e
 
git pull origin master
source myvenv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
