
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
from utils.subscription import handle_successful_subscription

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

app.secret_key = os.environ.get('SECRET_KEY', 'mystic_arcana_secret_key')
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_test_key')
webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_test_key')

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(readings_bp)
app.register_blueprint(astrology_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(blog_bp)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
