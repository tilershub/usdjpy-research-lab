#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

python -m pip install -r requirements-web.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py import_astro_content
python manage.py bootstrap_admin
