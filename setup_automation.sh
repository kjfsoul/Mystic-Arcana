
#!/bin/bash

# Install required packages
echo "Installing required packages..."
pip install python-crontab

# Make scripts executable
chmod +x cron_jobs.py
chmod +x setup_cron.py

# Run the cron setup
echo "Setting up cron job..."
python3 setup_cron.py

# Run the content update once to verify it works
echo "Running initial content update to verify setup..."
python3 cron_jobs.py

echo "Setup complete! The system will now automatically update content daily at 12 AM UTC."
