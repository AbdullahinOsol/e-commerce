#!/bin/bash

set -e

# Define variables
VENV_DIR="/var/www/e-commerce/venv"
PROJECT_DIR="/var/www/e-commerce"

cd "$PROJECT_DIR"

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
