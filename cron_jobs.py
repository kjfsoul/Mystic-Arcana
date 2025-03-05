
#!/usr/bin/env python3
import os
import sys
import time
import schedule
from datetime import datetime
from replit import db
from utils.content_automation import generate_daily_content

def job():
    """Daily content generation job"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting automated content update...")
    
    try:
        generate_daily_content()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Content update completed successfully")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error during content update: {e}")
    
    print("----------------------------------------")

def run_scheduler():
    """Run the scheduler process"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Content automation scheduler started")
    print("Scheduled to run daily at 12:00 AM UTC")
    
    # Schedule the job to run at midnight UTC
    schedule.every().day.at("00:00").do(job)
    
    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-once":
        # Run the job once for testing
        job()
    else:
        # Start the scheduler
        run_scheduler()
