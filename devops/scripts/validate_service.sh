#!/bin/bash

set -e

# Check Gunicorn status
echo "Checking Gunicorn service status..."
if sudo systemctl is-active --quiet gunicorn; then
    echo "Gunicorn service is running successfully."
else
    echo "Gunicorn service failed to start."
    exit 1
fi
