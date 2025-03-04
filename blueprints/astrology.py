
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from replit import db
from datetime import datetime
from utils.openai_client import generate_astrology_insight

astrology_bp = Blueprint('astrology', __name__, url_prefix='/astrology')

# Zodiac sign data
ZODIAC_SIGNS = [
    {"name": "Aries", "dates": "March 21 - April 19", "element": "Fire"},
    {"name": "Taurus", "dates": "April 20 - May 20", "element": "Earth"},
    {"name": "Gemini", "dates": "May 21 - June 20", "element": "Air"},
    {"name": "Cancer", "dates": "June 21 - July 22", "element": "Water"},
    {"name": "Leo", "dates": "July 23 - August 22", "element": "Fire"},
    {"name": "Virgo", "dates": "August 23 - September 22", "element": "Earth"},
    {"name": "Libra", "dates": "September 23 - October 22", "element": "Air"},
    {"name": "Scorpio", "dates": "October 23 - November 21", "element": "Water"},
    {"name": "Sagittarius", "dates": "November 22 - December 21", "element": "Fire"},
    {"name": "Capricorn", "dates": "December 22 - January 19", "element": "Earth"},
    {"name": "Aquarius", "dates": "January 20 - February 18", "element": "Air"},
    {"name": "Pisces", "dates": "February 19 - March 20", "element": "Water"}
]

@astrology_bp.route('/')
def astrology_home():
    # Create a featured insight if there's none today
    today = datetime.now().strftime("%Y-%m-%d")
    
    if 'daily_horoscopes' not in db:
        db['daily_horoscopes'] = {}
    
    if today not in db['daily_horoscopes']:
        # Generate a general cosmic insight for today
        from utils.openai_client import generate_completion
        prompt = f"""
        Generate a short general astrological insight for today ({today}).
        Focus on overall cosmic energy, lunar phase, and meaningful transits.
        Keep it under 250 words and format with basic HTML.
        """
        general_insight = generate_completion(prompt, max_tokens=500)
        
        db['daily_horoscopes'][today] = {
            "date": today,
            "general_insight": general_insight
        }
    
    daily_insight = db['daily_horoscopes'][today]
    featured_sign = "Libra"  # This could rotate or be personalized
    
    return render_template('astrology.html', 
                          zodiac_signs=ZODIAC_SIGNS,
                          daily_insight=daily_insight,
                          featured_sign=featured_sign)

@astrology_bp.route('/horoscope/<sign>')
def horoscope(sign):
    """Show horoscope for a specific zodiac sign"""
    # Find the zodiac sign info
    sign_info = next((s for s in ZODIAC_SIGNS if s['name'].lower() == sign.lower()), None)
    
    if not sign_info:
        return redirect(url_for('astrology.astrology_home'))
    
    # Check if we have a recent horoscope for this sign
    today = datetime.now().strftime("%Y-%m-%d")
    
    if 'ai_horoscopes' not in db:
        db['ai_horoscopes'] = {}
    
    # If we don't have today's horoscope for this sign, generate it
    if sign.lower() not in db['ai_horoscopes'] or 'generated_at' not in db['ai_horoscopes'][sign.lower()] or not db['ai_horoscopes'][sign.lower()]['generated_at'].startswith(today):
        horoscope_text = generate_astrology_insight(sign)
    else:
        horoscope_text = db['ai_horoscopes'][sign.lower()]['content']
    
    return render_template('horoscope.html', 
                          sign=sign_info,
                          horoscope=horoscope_text)

@astrology_bp.route('/premium')
def premium_astrology():
    """Premium astrology insights with detailed personalized readings"""
    from utils.subscription import is_premium_user
    
    # Check if user is authenticated
    if 'user_id' not in session:
        return redirect(url_for('profile.login', next=request.path))
    
    # Check if user has premium subscription
    if not is_premium_user(session['user_id']):
        return render_template('premium_upsell.html', 
                              service='astrology',
                              current_path=request.path)
    
    # Get user's zodiac sign from profile if available
    user_sign = None
    if 'users' in db and session['user_id'] in db['users']:
        user = db['users'][session['user_id']]
        if 'preferences' in user and 'zodiac_sign' in user['preferences']:
            user_sign = user['preferences']['zodiac_sign']
    
    # Get current planetary positions and transits
    from utils.openai_client import generate_completion
    prompt = f"""
    Generate a detailed current planetary positions report.
    Include the positions of all planets, significant aspects, and 
    current transits that affect all zodiac signs.
    Format with HTML and keep it under 500 words.
    """
    
    planetary_report = generate_completion(prompt, max_tokens=800)
    
    return render_template('premium_astrology.html',
                          zodiac_signs=ZODIAC_SIGNS,
                          user_sign=user_sign,
                          planetary_report=planetary_report)

@astrology_bp.route('/planet-alignment')
def planet_alignment():
    """Information about the upcoming seven-planet alignment of February 2025"""
    # Get or generate content about the alignment
    if 'planet_alignment' not in db:
        from utils.openai_client import generate_completion
        prompt = """
        Create a detailed guide about the Seven-Planet Alignment happening on February 28, 2025.
        Include:
        1. What makes this alignment special
        2. Which planets are involved
        3. Astrological significance
        4. How to best view it in the sky
        5. Spiritual practices to make the most of this rare event
        
        Format with HTML headings and paragraphs. Include scientific and mystical perspectives.
        """
        
        alignment_content = generate_completion(prompt, max_tokens=1500)
        
        db['planet_alignment'] = {
            "content": alignment_content,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    alignment_info = db['planet_alignment']
    
    return render_template('planet_alignment.html', 
                          alignment_info=alignment_info)
