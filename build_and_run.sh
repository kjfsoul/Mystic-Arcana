
#!/bin/bash

# Deployment script for Mystic Arcana
set -e  # Exit on any error

echo "Starting Mystic Arcana deployment setup..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize the database if needed
echo "Initializing database..."
python init_db.py

# Generate fresh content (initial content)
echo "Generating fresh content..."
python generate_fresh_content.py

# Test the Flask app imports
echo "Testing Flask app imports..."
python -c "from app import app; print('✅ Flask app imports successfully')"

# Set up the content scheduler
echo "Setting up automation..."
chmod +x cron_jobs.py
chmod +x setup_automation.sh

# Run a basic health check
echo "Running deployment tests..."
python test_deployment.py

echo "Deployment setup complete! Application is ready to start."
