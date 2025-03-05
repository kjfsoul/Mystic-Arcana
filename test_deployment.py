
#!/usr/bin/env python3
import requests
import sys
import os
import time
from datetime import datetime

def test_deployment():
    """Test if the deployment is functioning properly"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Testing Mystic Arcana deployment...")
    
    # Determine the base URL
    base_url = os.environ.get('REPL_SLUG', None)
    if base_url:
        base_url = f"https://{base_url}.replit.app"
    else:
        base_url = "http://localhost:5000"
    
    routes_to_test = [
        "/",
        "/readings",
        "/astrology",
        "/blog",
        "/profile/login",
    ]
    
    all_passed = True
    for route in routes_to_test:
        url = f"{base_url}{route}"
        try:
            print(f"Testing {url}...")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                print(f"✅ {route} - Success ({response.status_code})")
            else:
                print(f"❌ {route} - Failed ({response.status_code})")
                all_passed = False
        except Exception as e:
            print(f"❌ {route} - Error: {str(e)}")
            all_passed = False
    
    # Test content generation
    print("\nTesting content generation...")
    try:
        from utils.content_automation import generate_daily_content
        generate_daily_content(test_mode=True)
        print("✅ Content generation test passed")
    except Exception as e:
        print(f"❌ Content generation failed: {str(e)}")
        all_passed = False
    
    # Final results
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All deployment tests passed! Your application is ready.")
    else:
        print("⚠️ Some tests failed. Please check the logs and fix the issues.")
    
    return all_passed

if __name__ == "__main__":
    success = test_deployment()
    sys.exit(0 if success else 1)
