#!/bin/bash
echo "Starting Mystic Arcana application..."

# Install dependencies if needed
if [ ! -f ".dependencies_installed" ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
  touch .dependencies_installed
fi

# Setting up environment...
echo "Setting up environment..."
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

# Run the Flask application
exec python app.py
#!/bin/bash

# Kill any process running on port 3000
echo "Checking for processes on port 3000..."
npx kill-port 3000 || true

# Install dependencies
echo "Installing dependencies..."
npm install --force

# Build the React app
echo "Building React app..."
npm run build

# Start the server
echo "Starting server..."
npm start
