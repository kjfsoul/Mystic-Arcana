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

# Add error handler for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

# Add error handler for 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    # Ensure the Flask app runs on the correct host and port for deployment
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)