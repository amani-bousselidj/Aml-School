#!/bin/bash

source .v/bin/activate
gunicorn --workers 3 --bind :8000 Schoolproject.wsgi &
