
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from replit import db
import os
import json
import stripe
from datetime import datetime
from blueprints.home import home_bp
from blueprints.readings import readings_bp
from blueprints.astrology import astrology_bp
from blueprints.profile import profile_bp
from blueprints.blog import blog_bp
from blueprints.subscription import subscription_bp
from utils.subscription import handle_successful_subscription

app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')

# Load secrets from Replit Secrets
from os import environ as env
app.secret_key = env.get('SECRET_KEY', 'mystic_arcana_secret_key')
stripe.api_key = env.get('STRIPE_SECRET_KEY', 'sk_test_your_test_key')
webhook_secret = env.get('STRIPE_WEBHOOK_SECRET', 'whsec_test_key')
openai_api_key = env.get('OPENAI_API_KEY', 'your_openai_api_key')

# Log startup configuration (without sensitive values)
print("Flask app starting with configuration:")
print(f"- SECRET_KEY: {'[Set]' if 'SECRET_KEY' in env else '[Using Default]'}")
print(f"- STRIPE_SECRET_KEY: {'[Set]' if 'STRIPE_SECRET_KEY' in env else '[Using Default]'}")
print(f"- STRIPE_WEBHOOK_SECRET: {'[Set]' if 'STRIPE_WEBHOOK_SECRET' in env else '[Using Default]'}")
print(f"- OPENAI_API_KEY: {'[Set]' if 'OPENAI_API_KEY' in env else '[Using Default]'}")

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(astrology_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(subscription_bp)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': str(e)}), 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase
        handle_successful_subscription(session)

    return jsonify({'status': 'success'})

@app.context_processor
def inject_user_premium_status():
    """Add premium status to templates"""
    from utils.subscription import is_premium_user
    
    premium = False
    if 'user_id' in session:
        premium = is_premium_user(session['user_id'])
    
    return {'is_premium': premium}

def start_scheduler_in_background():
    """Start the content scheduler as a background process"""
    import subprocess
    import os
    import sys
    import threading
    
    try:
        # Check if we're in a production environment (Replit deployment)
        if os.environ.get('REPL_SLUG') or os.environ.get('REPLIT_DEPLOYMENT'):
            print("Starting content scheduler in background...")
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Check if the scheduler is already running
            try:
                with open('scheduler.pid', 'r') as f:
                    pid = int(f.read().strip())
                    try:
                        # Check if process is still running
                        os.kill(pid, 0)
                        print(f"Scheduler already running with PID {pid}")
                        return
                    except OSError:
                        # Process not running, continue with startup
                        pass
            except FileNotFoundError:
                # PID file doesn't exist, continue with startup
                pass
                
            # Start the scheduler and save PID
            if os.environ.get('REPLIT_DEPLOYMENT'):
                # In deployment, use threading to avoid issues with subprocess
                def run_scheduler():
                    with open('scheduler.log', 'a') as log_file:
                        sys.stdout = log_file
                        sys.stderr = log_file
                        import cron_jobs
                        cron_jobs.run_scheduler()
                
                print("Starting scheduler in deployment mode using threading")
                scheduler_thread = threading.Thread(target=run_scheduler)
                scheduler_thread.daemon = True
                scheduler_thread.start()
                print("Content scheduler started in background thread!")
            else:
                # Start the scheduler and save PID (development mode)
                process = subprocess.Popen([
                    'python3', 
                    os.path.join(script_dir, 'cron_jobs.py')
                ], 
                stdout=open('scheduler.log', 'a'),
                stderr=subprocess.STDOUT,
                start_new_session=True)
                
                # Save PID to file for future reference
                with open('scheduler.pid', 'w') as f:
                    f.write(str(process.pid))
                    
                print(f"Content scheduler started with PID {process.pid}!")
    except Exception as e:
        print(f"Failed to start content scheduler: {e}")

if __name__ == '__main__':
    # Only start the scheduler in the main process when deployed
    if os.environ.get('REPL_ID'):
        start_scheduler_in_background()
    
    # Use port 5000 for Autoscale deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
