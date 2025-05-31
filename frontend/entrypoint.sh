#!/bin/bash

python manage.py collectstatic --noinput
cp -r /frontend/static/* /static/ || echo "---------Static files copy skipped---------"

exec "$@"
