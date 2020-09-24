#!/bin/bash
export DJANGO_SETTINGS_MODULE="back-end.settings.development"
cd back-end/
python manage.py runserver