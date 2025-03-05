
#!/bin/bash

# Install required packages
echo "Installing required packages..."
pip install schedule replit

# Make scripts executable
chmod +x cron_jobs.py

# Run the content update once to verify it works
echo "Running initial content update to verify setup..."
python3 cron_jobs.py --run-once

echo "Setup complete! The script will automatically update content daily at 12 AM UTC."
echo "To start the background scheduler, run: python3 cron_jobs.py &"
