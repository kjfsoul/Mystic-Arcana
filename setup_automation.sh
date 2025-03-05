
#!/bin/bash

# Install required packages
echo "Installing required packages..."
pip install schedule replit

# Make scripts executable
chmod +x cron_jobs.py
chmod +x generate_fresh_content.py

# Function to check if the scheduler is already running
check_scheduler() {
  if pgrep -f "python cron_jobs.py" > /dev/null; then
    echo "Content scheduler is already running!"
    return 0
  else
    return 1
  fi
}

# Function to start the scheduler
start_scheduler() {
  echo "Starting content scheduler in background..."
  nohup python cron_jobs.py > scheduler.log 2>&1 &
  echo "Content scheduler started with PID $!"
}

# Run the content update once to verify it works
echo "Running initial content update to verify setup..."
python generate_fresh_content.py

# Check if scheduler is running, if not start it
if ! check_scheduler; then
  start_scheduler
fi

echo "Setup complete! The script will automatically update content daily at 12 AM UTC."
echo "Check scheduler.log for output from the scheduler process."
echo "To restart the scheduler, run this script again or manually run: nohup python cron_jobs.py > scheduler.log 2>&1 &"
