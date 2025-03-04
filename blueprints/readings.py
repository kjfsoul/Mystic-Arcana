
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from replit import db
from datetime import datetime
import random
import json

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
    return render_template('readings.html')

@readings_bp.route('/new', methods=['POST'])
def new_reading():
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    # Generate a simple 3-card reading
    cards = random.sample(TAROT_CARDS, 3)
    reading = {
        "user_id": session['user_id'],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cards": cards,
        "question": request.form.get('question', 'General guidance'),
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
