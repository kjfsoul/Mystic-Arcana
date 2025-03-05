
#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
from utils.content_automation import generate_daily_content

def run_content_update():
    """Run the content update process and log results"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting automated content update...")
    
    try:
        generate_daily_content()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Content update completed successfully")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error during content update: {e}")
    
    print("----------------------------------------")

if __name__ == "__main__":
    run_content_update()
