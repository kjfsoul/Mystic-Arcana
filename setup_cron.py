
#!/usr/bin/env python3
import os
import sys
from crontab import CronTab

def setup_cron_job():
    """Set up a cron job to run daily at 12 AM UTC"""
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create a cron job for the current user
        cron = CronTab(user=True)
        
        # Remove any existing jobs with the same comment
        for job in cron.find_comment('mystic_arcana_content_update'):
            cron.remove(job)
            print("Removed existing cron job")
        
        # Create a new job
        job = cron.new(command=f'cd {current_dir} && python3 {current_dir}/cron_jobs.py >> {current_dir}/cron.log 2>&1')
        job.setall('0 0 * * *')  # Run at 12 AM UTC every day
        job.set_comment('mystic_arcana_content_update')
        
        # Write the crontab
        cron.write()
        
        print("✅ Cron job set up successfully to run daily at 12 AM UTC")
        print(f"Cron job command: {job.command}")
        print("Check cron.log file for execution logs")
    except Exception as e:
        print(f"❌ Error setting up cron job: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_cron_job()
