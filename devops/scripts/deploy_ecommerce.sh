#!/bin/bash

set -e

# Define variables from Jenkins environment
WORKSPACE="$WORKSPACE"          # Jenkins workspace (automatically populated)
DESTINATION="$DESTINATION"      # Destination directory on EC2 (from Jenkins environment)
PUBLIC_IP="$PUBLIC_IP"          # EC2 Public IP (from Jenkins environment)
SSH_KEY_FILE="$SSH_KEY_FILE"    # SSH key file (from Jenkins environment)
SSH_USERNAME="$SSH_USERNAME"    # SSH username (from Jenkins environment)

# Check if required Jenkins variables are set
if [[ -z "$WORKSPACE" || -z "$DESTINATION" || -z "$PUBLIC_IP" || -z "$SSH_KEY_FILE" || -z "$SSH_USERNAME" ]]; then
    echo "Error: Missing required Jenkins environment variables."
    echo "Ensure WORKSPACE, DESTINATION, PUBLIC_IP, SSH_KEY_FILE, and SSH_USERNAME are set."
    exit 1
fi

# Rsync the latest code from Jenkins workspace to the EC2 server
echo "Syncing files from Jenkins workspace ($WORKSPACE) to EC2 destination ($DESTINATION)..."
rsync -avzu -e "ssh -i $SSH_KEY_FILE" "$WORKSPACE" "$SSH_USERNAME@$PUBLIC_IP:$DESTINATION"

# Execute the remote deployment script on EC2 server
echo "Executing remote deployment script on EC2 server..."
ssh -i "$SSH_KEY_FILE" "$SSH_USERNAME@$PUBLIC_IP" "bash $DESTINATION/devops/scripts/install_dependencies.sh"
ssh -i "$SSH_KEY_FILE" "$SSH_USERNAME@$PUBLIC_IP" "bash $DESTINATION/devops/scripts/migrate_db.sh"
ssh -i "$SSH_KEY_FILE" "$SSH_USERNAME@$PUBLIC_IP" "bash $DESTINATION/devops/scripts/start_server.sh"
ssh -i "$SSH_KEY_FILE" "$SSH_USERNAME@$PUBLIC_IP" "bash $DESTINATION/devops/scripts/validate_service.sh"

