
#!/bin/bash

# Deployment script for Mystic Arcana

echo "Starting Mystic Arcana deployment setup..."

# Install dependencies
pip install -r requirements.txt

# Initialize the database if needed
python init_db.py

# Generate fresh content (initial content)
python generate_fresh_content.py

# Set up the content scheduler
chmod +x cron_jobs.py
chmod +x setup_automation.sh

echo "Deployment setup complete! Application will start with 'python app.py'"
