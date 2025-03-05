
#!/usr/bin/env python3
import os
import sys
import subprocess

def setup_automation():
    """Set up the content automation as a background task"""
    try:
        print("Setting up Mystic Arcana content automation...")
        
        # Create a nohup startup script
        startup_script = '''#!/bin/bash
cd {}
nohup python3 cron_jobs.py > automation.log 2>&1 &
echo $! > automation.pid
echo "Content automation started with PID $(cat automation.pid)"
'''.format(os.path.dirname(os.path.abspath(__file__)))
        
        with open('start_automation.sh', 'w') as f:
            f.write(startup_script)
        
        # Make it executable
        os.chmod('start_automation.sh', 0o755)
        
        print("✅ Automation setup complete!")
        print("To start the automation service, run: ./start_automation.sh")
        print("The service will run in the background and update content daily at 12 AM UTC")
        
    except Exception as e:
        print(f"❌ Error setting up automation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_automation()
