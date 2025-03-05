
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from replit import db
import stripe
from utils.subscription import create_checkout_session, is_premium_user

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription_bp.route('/checkout')
def checkout():
    """Create a checkout session for premium subscription"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('profile.login', next=request.path))
        
    # If already premium, redirect to account
    if is_premium_user(session['user_id']):
        return redirect(url_for('profile.account', message='You already have an active subscription'))
    
    # Set success and cancel URLs
    success_url = url_for('subscription.success', _external=True)
    cancel_url = url_for('subscription.cancel', _external=True)
    
    # Create checkout session
    checkout_session = create_checkout_session(
        user_id=session['user_id'],
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    if not checkout_session:
        # If checkout creation failed
        return render_template('error.html', 
                              error="Unable to create checkout session. Please try again later.")
    
    # Redirect to Stripe checkout
    return redirect(checkout_session.url)

@subscription_bp.route('/success')
def success():
    """Handle successful subscription"""
    return render_template('subscription_success.html')

@subscription_bp.route('/cancel')
def cancel():
    """Handle cancelled subscription attempt"""
    return redirect(url_for('readings.premium', message='Subscription process was cancelled'))

@subscription_bp.route('/manage')
def manage():
    """Manage existing subscription"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    # Check if user has subscription
    if not is_premium_user(session['user_id']):
        return redirect(url_for('subscription.checkout'))
    
    # Get subscription details
    subscription_data = None
    if 'subscriptions' in db and session['user_id'] in db['subscriptions']:
        subscription_data = db['subscriptions'][session['user_id']]
    
    return render_template('manage_subscription.html', subscription=subscription_data)

@subscription_bp.route('/cancel_subscription', methods=['POST'])
def cancel_subscription():
    """Cancel user subscription"""
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    from utils.subscription import cancel_subscription as cancel_sub
    result = cancel_sub(session['user_id'])
    
    if result:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to cancel subscription'}), 500
