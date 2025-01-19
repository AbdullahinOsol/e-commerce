#!/bin/bash

set -e

# Define variables from Jenkins environment
DESTINATION="$DESTINATION"  # Destination directory on EC2
PUBLIC_IP="$PUBLIC_IP"          # EC2 Public IP (from Jenkins environment)
SSH_KEY_FILE="$SSH_KEY_FILE"    # SSH key file (from Jenkins environment)
SSH_USERNAME="$SSH_USERNAME"    # SSH username (from Jenkins environment)

# Check if required Jenkins variables are set
if [[ -z "$WORKSPACE" || -z "$DESTINATION" || -z "$PUBLIC_IP" || -z "$SSH_KEY_FILE" || -z "$SSH_USERNAME" ]]; then
    echo "Error: Missing required Jenkins environment variables."
    echo "Ensure WORKSPACE, DESTINATION, PUBLIC_IP, SSH_KEY_FILE, and SSH_USERNAME are set."
    exit 1
fi

# Rsync the latest code from Jenkins workspace to the EC2 server's destination directory
echo "Syncing files from Jenkins workspace ($WORKSPACE) to EC2 destination ($DESTINATION)..."
rsync -avzu -e "ssh -i $SSH_KEY_FILE" "$WORKSPACE/" "$SSH_USERNAME@$PUBLIC_IP:$DESTINATION"

# Execute the deploy_ecommerce.sh script in the destination directory on the EC2 instance
echo "Executing deployment process on EC2 server..."

# Now we're inside the destination directory on EC2: /var/www/e-commerce
ssh -i "$SSH_KEY_FILE" "$SSH_USERNAME@$PUBLIC_IP" << EOF
cd $DESTINATION/devops/scripts

# Execute all the necessary scripts one by one
echo "Starting deployment steps..."

# Install dependencies
bash install_dependencies.sh

# Run database migrations and collect static files
bash migrate_db.sh

# Start the server (e.g., Gunicorn or other services)
bash start_server.sh

# Validate the service status (e.g., Gunicorn status)
bash validate_service.sh
EOF
