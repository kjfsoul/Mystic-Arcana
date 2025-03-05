
#!/bin/bash

# Deployment script for Mystic Arcana

echo "Starting Mystic Arcana deployment..."

# Install dependencies
pip install -r requirements.txt

# Initialize the database if needed
python init_db.py

# Generate fresh content (initial content)
python generate_fresh_content.py

# Start the content scheduler
python app.py &

echo "Deployment complete! Application is running."
