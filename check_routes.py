
#!/usr/bin/env python3
import requests
import sys
import os

def check_routes():
    """Check if all main routes are functioning properly"""
    base_url = os.environ.get('REPL_SLUG', 'https://mysticarcana.replit.app')
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}.replit.app"
    
    routes = [
        "/",
        "/readings",
        "/astrology",
        "/blog",
        "/profile/login"
    ]
    
    print(f"Checking routes on {base_url}...")
    
    failed = False
    for route in routes:
        try:
            url = f"{base_url}{route}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {route} - OK (200)")
            else:
                print(f"❌ {route} - Failed ({response.status_code})")
                failed = True
        except Exception as e:
            print(f"❌ {route} - Error: {e}")
            failed = True
    
    if failed:
        print("Some routes are not functioning correctly. Please check the application logs.")
        return False
    else:
        print("All routes are functioning correctly!")
        return True

if __name__ == "__main__":
    success = check_routes()
    sys.exit(0 if success else 1)
