
import os
import stripe
from replit import db
from datetime import datetime, timedelta

# Initialize Stripe - Using Replit Secrets for API key
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
if not stripe.api_key:
    print("WARNING: Stripe API key not found in secrets. Subscription features will not work.")

def create_checkout_session(user_id, success_url, cancel_url):
    """
    Create a Stripe checkout session for monthly subscription
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Mystic Arcana Premium',
                            'description': 'Monthly subscription for premium mystic insights',
                        },
                        'unit_amount': 500, # $5.00 in cents
                        'recurring': {
                            'interval': 'month',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=user_id,
        )
        return checkout_session
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return None

def handle_successful_subscription(session):
    """
    Process a successful subscription payment
    """
    user_id = session.get('client_reference_id')
    subscription_id = session.get('subscription')
    
    if not user_id:
        return False
    
    # Initialize subscriptions in db if not exists
    if 'subscriptions' not in db:
        db['subscriptions'] = {}
    
    # Add subscription to database
    db['subscriptions'][user_id] = {
        'subscription_id': subscription_id,
        'status': 'active',
        'start_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'end_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return True

def is_premium_user(user_id):
    """
    Check if a user has an active premium subscription
    """
    if not user_id or 'subscriptions' not in db:
        return False
    
    # Check if user has a subscription and it's active
    if user_id in db['subscriptions'] and db['subscriptions'][user_id]['status'] == 'active':
        # Check if subscription is still valid
        end_date = datetime.strptime(db['subscriptions'][user_id]['end_date'], "%Y-%m-%d %H:%M:%S")
        if end_date > datetime.now():
            return True
        else:
            # Update status to expired
            db['subscriptions'][user_id]['status'] = 'expired'
    
    return False

def cancel_subscription(user_id):
    """
    Cancel a user's subscription
    """
    if not user_id or 'subscriptions' not in db or user_id not in db['subscriptions']:
        return False
    
    subscription_id = db['subscriptions'][user_id].get('subscription_id')
    if not subscription_id:
        return False
    
    try:
        # Cancel the subscription in Stripe
        stripe.Subscription.delete(subscription_id)
        
        # Update subscription status in database
        db['subscriptions'][user_id]['status'] = 'cancelled'
        return True
    except Exception as e:
        print(f"Error canceling subscription: {e}")
        return False
