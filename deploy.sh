#!/bin/bash
set -e

cd romanchenkodv.pythonanywhere.com 
git pull origin dev
source myvenv/bin/activate
pip install -r requirements
python manage.py migrate
python manage.py collectstatic --noinput
