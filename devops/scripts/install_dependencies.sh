#!/bin/bash

set -e

# Define variables
VENV_DIR="/var/www/e-commerce/venv"
PROJECT_DIR="/var/www/e-commerce"

cd "$PROJECT_DIR"

echo "Starting deployment process..."

# Activate virtual environment if it exists, or create a new one
if [ -d "$VENV_DIR" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "Virtual environment created successfully."
        source "$VENV_DIR/bin/activate"
    else
        echo "Failed to create the virtual environment. Please check for errors."
        exit 1
    fi
fi

# Install dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt
echo "Installation completed successfully."
