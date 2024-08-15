#!/bin/bash

# Navigate to the project directory
cd /path/to/your/project || exit

# Pull the latest changes from the main branch (if using Git)
git pull origin main

#  Activate the virtual environment
source venv/bin/activate

#  Install or update Python dependencies
pip install -r requirements.txt

#  Run database migrations
flask db upgrade


#  Restart the application service

sudo systemctl restart YogaSequencingApp1.service

# Log the deployment
echo "Deployment completed at $(date)" >> deployment.log
