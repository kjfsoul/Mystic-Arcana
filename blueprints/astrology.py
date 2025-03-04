
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from replit import db
from datetime import datetime
from utils.openai_client import generate_astrology_insight

astrology_bp = Blueprint('astrology', __name__, url_prefix='/astrology')

ZODIAC_SIGNS = {
    "aries": {"dates": "March 21 - April 19", "element": "Fire", "ruling_planet": "Mars"},
    "taurus": {"dates": "April 20 - May 20", "element": "Earth", "ruling_planet": "Venus"},
    "gemini": {"dates": "May 21 - June 20", "element": "Air", "ruling_planet": "Mercury"},
    "cancer": {"dates": "June 21 - July 22", "element": "Water", "ruling_planet": "Moon"},
    "leo": {"dates": "July 23 - August 22", "element": "Fire", "ruling_planet": "Sun"},
    "virgo": {"dates": "August 23 - September 22", "element": "Earth", "ruling_planet": "Mercury"},
    "libra": {"dates": "September 23 - October 22", "element": "Air", "ruling_planet": "Venus"},
    "scorpio": {"dates": "October 23 - November 21", "element": "Water", "ruling_planet": "Pluto"},
    "sagittarius": {"dates": "November 22 - December 21", "element": "Fire", "ruling_planet": "Jupiter"},
    "capricorn": {"dates": "December 22 - January 19", "element": "Earth", "ruling_planet": "Saturn"},
    "aquarius": {"dates": "January 20 - February 18", "element": "Air", "ruling_planet": "Uranus"},
    "pisces": {"dates": "February 19 - March 20", "element": "Water", "ruling_planet": "Neptune"}
}

# Default horoscopes will be used as fallback when AI is unavailable
DAILY_HOROSCOPES = {
    "aries": "Today is a great day for new beginnings. Your energy is high, and you can accomplish a lot if you stay focused.",
    "taurus": "Stability is key today. Focus on self-care and building your resources. A financial opportunity may arise.",
    "gemini": "Communication is highlighted today. Share your ideas and connect with others - valuable insights await.",
    "cancer": "Your intuition is especially strong today. Trust your gut feelings and take care of your emotional needs.",
    "leo": "Your creative energy is flowing. Express yourself boldly and don't be afraid to take center stage.",
    "virgo": "Details matter today. Your analytical skills will help you solve problems and improve systems.",
    "libra": "Harmony in relationships is important today. Find balance between your needs and others'.",
    "scorpio": "Transformation is in the air. Let go of what no longer serves you and embrace personal power.",
    "sagittarius": "Adventure calls! Explore new ideas, places, or philosophies that expand your horizons.",
    "capricorn": "Focus on long-term goals today. Your discipline and practical approach will bring success.",
    "aquarius": "Innovation is your strength today. Think outside the box and connect with like-minded people.",
    "pisces": "Your imagination is powerful today. Creative pursuits and spiritual practices are especially rewarding."
}

@astrology_bp.route('/')
def astrology_home():
    # Check if we have AI-generated horoscopes for today
    today = datetime.now().strftime("%Y-%m-%d")
    has_ai_horoscopes = 'ai_horoscopes' in db and bool(db['ai_horoscopes'])
    
    return render_template('astrology.html', 
                          zodiac_signs=ZODIAC_SIGNS,
                          has_ai_horoscopes=has_ai_horoscopes)

@astrology_bp.route('/horoscope/<sign>')
def horoscope(sign):
    if sign.lower() not in ZODIAC_SIGNS:
        return redirect(url_for('astrology.astrology_home'))
    
    use_ai = request.args.get('ai', 'true').lower() == 'true'
    sign_info = ZODIAC_SIGNS.get(sign.lower(), {})
    
    # Check if we have an AI-generated horoscope for this sign
    if use_ai and 'ai_horoscopes' in db and sign.lower() in db['ai_horoscopes']:
        horoscope_data = db['ai_horoscopes'][sign.lower()]
        # Check if the horoscope is from today, if not, generate a new one
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in horoscope_data.get('generated_at', ''):
            horoscope_text = generate_astrology_insight(sign)
        else:
            horoscope_text = horoscope_data['content']
    elif use_ai:
        # Generate a new AI horoscope
        horoscope_text = generate_astrology_insight(sign)
    else:
        # Use the default static horoscope
        horoscope_text = DAILY_HOROSCOPES.get(sign.lower(), "Horoscope not available")
    
    return render_template('horoscope.html', 
                          sign=sign.capitalize(), 
                          horoscope=horoscope_text,
                          sign_info=sign_info,
                          is_ai_generated=use_ai)

@astrology_bp.route('/planet-alignment')
def planet_alignment():
    # Check if we have an AI-generated content about planet alignment
    if 'ai_planet_alignment' not in db:
        from utils.openai_client import generate_completion
        
        prompt = """
        Generate an informative article about the upcoming seven-planet alignment of 2025.
        Include astronomical facts, viewing tips, and astrological significance.
        Format with HTML tags for proper display.
        """
        
        content = generate_completion(prompt, max_tokens=2000)
        
        db['ai_planet_alignment'] = {
            "content": content,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    alignment_content = db['ai_planet_alignment']['content']
    return render_template('planet_alignment.html', alignment_content=alignment_content)

@astrology_bp.route('/generate-all-horoscopes', methods=['POST'])
def generate_all_horoscopes():
    """Admin route to generate all horoscopes using AI"""
    if 'user_id' not in session:
        return redirect(url_for('profile.login'))
    
    # For security, only allow admins to trigger this
    if 'users' in db and session['user_id'] in db['users']:
        user = db['users'][session['user_id']]
        if user.get('email') != 'admin@mysticarcana.com':
            return redirect(url_for('astrology.astrology_home'))
    
    # Generate horoscopes for all signs
    for sign in ZODIAC_SIGNS:
        generate_astrology_insight(sign)
    
    return redirect(url_for('astrology.astrology_home'))
