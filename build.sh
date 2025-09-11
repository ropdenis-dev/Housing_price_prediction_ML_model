#!/usr/bin/env bash
# build.sh
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Collect static files
python manage.py collectstatic --noinput