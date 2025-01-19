#!/bin/bash

set -e

# Restart Gunicorn and Nginx services
echo "Restarting Gunicorn and Nginx services..."
sudo systemctl restart gunicorn
sudo systemctl reload nginx
