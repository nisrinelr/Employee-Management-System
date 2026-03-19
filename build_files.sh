#!/bin/bash
set -e

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Creating static directories..."
mkdir -p staticfiles_build/static

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear
