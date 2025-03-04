
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from replit import db
from datetime import datetime
import random
import json
from utils.openai_client import generate_tarot_reading

readings_bp = Blueprint('readings', __name__, url_prefix='/readings')

# Tarot card data
TAROT_CARDS = [
    {"name": "The Fool", "meaning": "New beginnings, innocence, spontaneity"},
    {"name": "The Magician", "meaning": "Manifestation, resourcefulness, power"},
    {"name": "The High Priestess", "meaning": "Intuition, unconscious, inner voice"},
    {"name": "The Empress", "meaning": "Femininity, beauty, nature, abundance"},
    {"name": "The Emperor", "meaning": "Authority, structure, control, leadership"},
    {"name": "The Hierophant", "meaning": "Tradition, conformity, morality, ethics"},
    {"name": "The Lovers", "meaning": "Love, harmony, relationships, values alignment"},
    {"name": "The Chariot", "meaning": "Control, willpower, success, action"},
    {"name": "Strength", "meaning": "Courage, persuasion, influence, compassion"},
    {"name": "The Hermit", "meaning": "Soul-searching, introspection, guidance"},
    {"name": "Wheel of Fortune", "meaning": "Good luck, karma, destiny, a turning point"},
    {"name": "Justice", "meaning": "Justice, fairness, truth, law"},
    {"name": "The Hanged Man", "meaning": "Surrender, letting go, new perspective"},
    {"name": "Death", "meaning": "Endings, change, transformation, transition"},
    {"name": "Temperance", "meaning": "Balance, moderation, patience, purpose"},
    {"name": "The Devil", "meaning": "Shadow self, attachment, addiction, restriction"},
    {"name": "The Tower", "meaning": "Sudden change, upheaval, chaos, revelation"},
    {"name": "The Star", "meaning": "Hope, faith, purpose, renewal, spirituality"},
    {"name": "The Moon", "meaning": "Illusion, fear, anxiety, subconscious"},
    {"name": "The Sun", "meaning": "Positivity, fun, warmth, success"},
    {"name": "Judgment", "meaning": "Judgment, rebirth, inner calling, absolution"},
    {"name": "The World", "meaning": "Completion, accomplishment, travel, harmony"}
]

@readings_bp.route('/')
def tarot_readings():
    # Get today's featured AI reading if available
    featured_reading = None
    if 'ai_readings' in db and db['ai_readings']:
        featured_reading = db['ai_readings'][-1]
    
    return render_template('readings.html', featured_reading=featured_reading)

@readings_bp.route('/premium')
def premium_readings():
    """Premium tarot readings page with advanced AI interpretations"""
    from utils.subscription import is_premium_user
    
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('profile.login', next=request.path))
    
    # Check if user has premium subscription
    if not is_premium_user(session['user_id']):
        return render_template('premium_upsell.html', 
                              service='readings',
                              current_path=request.path)
    
    # Get premium AI readings
    premium_readings = []
    if 'premium_readings' in db:
        # Get the last 5 premium readings
        premium_readings = db.get('premium_readings', [])[-5:]
    
    return render_template('premium_readings.html', 
                          premium_readings=premium_readings)

@readings_bp.route('/premium/new', methods=['POST'])
def new_premium_reading():
    """Generate a new premium reading with detailed AI insights"""
    from utils.subscription import is_premium_user
    
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    # Check if user has premium subscription
    if not is_premium_user(session['user_id']):
        return redirect(url_for('readings.premium'))
    
    question = request.form.get('question', 'Deep spiritual guidance')
    spread_type = request.form.get('spread_type', 'celtic')
    
    # Use more advanced AI prompt based on the chosen spread
    if spread_type == 'celtic':
        # Generate a Celtic Cross spread (10 cards)
        from utils.openai_client import generate_celtic_cross_reading
        ai_result = generate_celtic_cross_reading(question)
    else:
        # Default to a 5-card advanced spread
        from utils.openai_client import generate_detailed_reading
        ai_result = generate_detailed_reading(question, cards=5)
    
    reading = {
        "user_id": session['user_id'],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cards": ai_result["cards"],
        "question": question,
        "spread_type": spread_type,
        "ai_reading": ai_result["reading"],
        "premium": True,
        "id": str(datetime.now().timestamp())
    }
    
    # Store reading in database
    if 'premium_readings' not in db:
        db['premium_readings'] = []
    
    db['premium_readings'].append(reading)
    
    # Also add to user's history
    if 'readings' not in db:
        db['readings'] = {}
    
    if session['user_id'] not in db['readings']:
        db['readings'][session['user_id']] = []
    
    db['readings'][session['user_id']].append(reading)
    
    return render_template('premium_reading_result.html', reading=reading)

@readings_bp.route('/new', methods=['POST'])
def new_reading():
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    question = request.form.get('question', 'General guidance')
    use_ai = request.form.get('use_ai') == 'on'
    
    if use_ai:
        # Use the OpenAI integration for the reading
        ai_result = generate_tarot_reading(question)
        
        reading = {
            "user_id": session['user_id'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cards": ai_result["cards"],
            "question": question,
            "ai_reading": ai_result["reading"],
            "id": str(datetime.now().timestamp())
        }
    else:
        # Generate a simple 3-card reading without AI
        cards = random.sample(TAROT_CARDS, 3)
        reading = {
            "user_id": session['user_id'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cards": cards,
            "question": question,
            "id": str(datetime.now().timestamp())
        }
    
    # Store reading in database
    if 'readings' not in db:
        db['readings'] = {}
    
    if session['user_id'] not in db['readings']:
        db['readings'][session['user_id']] = []
    
    db['readings'][session['user_id']].append(reading)
    
    return render_template('reading_result.html', reading=reading)

@readings_bp.route('/history')
def reading_history():
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    user_readings = db['readings'].get(session['user_id'], []) if 'readings' in db else []
    return render_template('reading_history.html', readings=user_readings)

@readings_bp.route('/daily')
def daily_reading():
    """Get the daily tarot reading generated by AI"""
    # Check if we already have a daily reading for today
    today = datetime.now().strftime("%Y-%m-%d")
    
    if 'daily_readings' not in db:
        db['daily_readings'] = {}
    
    if today not in db['daily_readings']:
        # Generate a new daily reading
        ai_result = generate_tarot_reading("What energies are present for everyone today?")
        db['daily_readings'][today] = {
            "date": today,
            "cards": ai_result["cards"],
            "reading": ai_result["reading"]
        }
    
    daily_reading = db['daily_readings'][today]
    return render_template('daily_reading.html', reading=daily_reading)
